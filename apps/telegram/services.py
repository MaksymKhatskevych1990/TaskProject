"""Telegram business operations."""

import logging
from math import ceil
from typing import Any
from uuid import UUID

from django.contrib.auth import get_user_model

from apps.telegram import client
from apps.telegram.exceptions import TelegramAPIError, TelegramDisabledError
from apps.telegram.keyboards import (
    HISTORY_PAGE_SIZE,
    MENU_HELP_BUTTON,
    MENU_TASKS_BUTTON,
    build_main_menu_keyboard,
    build_project_history_keyboard,
    build_task_detail_keyboard,
    build_task_history_keyboard,
    build_task_keyboard,
    parse_history_callback,
    parse_task_callback_data,
    project_label,
)
from apps.telegram.models import TelegramAccount
from apps.telegram import selectors as telegram_selectors

logger = logging.getLogger(__name__)

User = get_user_model()

TELEGRAM_FIELDS = {"telegram_username", "telegram_chat_id", "telegram_notifications_enabled"}


def normalize_username(value: str) -> str:
    """Store Telegram usernames without the leading @ symbol."""
    return value.strip().lstrip("@")


def ensure_telegram_account(*, user: User) -> TelegramAccount:
    """Create a Telegram account record when one does not exist yet."""
    account, created = TelegramAccount.objects.get_or_create(user=user)
    if created:
        logger.info(
            "Created Telegram account placeholder",
            extra={"user_uuid": str(user.uuid)},
        )
    return account


def update_telegram_account(
    *,
    user: User,
    data: dict[str, Any],
    actor: User | None = None,
) -> TelegramAccount:
    """Update Telegram contact data for a user."""
    account = ensure_telegram_account(user=user)
    updates: dict[str, Any] = {}

    if "telegram_username" in data:
        updates["username"] = normalize_username(data["telegram_username"])
    if "telegram_chat_id" in data:
        updates["chat_id"] = data["telegram_chat_id"]
    if "telegram_notifications_enabled" in data:
        updates["notifications_enabled"] = data["telegram_notifications_enabled"]

    if not updates:
        return account

    for field, value in updates.items():
        setattr(account, field, value)
    if actor is not None:
        account.updated_by = actor
    account.save()
    logger.info(
        "Updated Telegram account",
        extra={"user_uuid": str(user.uuid), "chat_id": account.chat_id},
    )
    return account


def send_telegram_message(
    *,
    chat_id: int,
    text: str,
    reply_markup: dict[str, Any] | None = None,
) -> bool:
    """Send a message through the Telegram Bot API."""
    try:
        client.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
    except TelegramDisabledError:
        logger.info(
            "Skipped Telegram message because integration is disabled",
            extra={"chat_id": chat_id},
        )
        return False
    except TelegramAPIError:
        logger.exception("Failed to send Telegram message", extra={"chat_id": chat_id})
        raise
    return True


def queue_telegram_message(
    *,
    chat_id: int,
    text: str,
    reply_markup: dict[str, Any] | None = None,
) -> None:
    """Enqueue a Telegram message for asynchronous delivery."""
    from apps.telegram.tasks import send_telegram_message_task

    send_telegram_message_task.delay(chat_id, text, reply_markup)


def link_account_by_token(
    *,
    token: str,
    chat_id: int,
    username: str = "",
) -> TelegramAccount | None:
    """Bind a Telegram chat to a studio user using a one-time link token."""
    account = (
        TelegramAccount.objects.select_related("user")
        .filter(link_token=token)
        .first()
    )
    if account is None:
        send_telegram_message(
            chat_id=chat_id,
            text="Ссылка недействительна. Попросите администратора прислать новую.",
        )
        return None

    update_telegram_account(
        user=account.user,
        data={
            "telegram_chat_id": chat_id,
            "telegram_username": username,
            "telegram_notifications_enabled": True,
        },
    )
    account.refresh_from_db()
    send_telegram_message(
        chat_id=chat_id,
        text=(
            f"Аккаунт привязан к {account.user.email}.\n"
            "Теперь вы будете получать задачи в этот чат.\n\n"
            "Используйте кнопку «Мои задачи», чтобы смотреть историю заданий."
        ),
        reply_markup=build_main_menu_keyboard(),
    )
    return account


def process_webhook_update(*, update: dict[str, Any]) -> None:
    """Handle an incoming Telegram update."""
    callback_query = update.get("callback_query")
    if callback_query:
        process_callback_query(callback_query=callback_query)
        return

    message = update.get("message") or update.get("edited_message")
    if not message:
        return

    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    if chat_id is None:
        return

    text = (message.get("text") or "").strip()
    from_user = message.get("from") or {}
    username = from_user.get("username") or ""

    account = _resolve_account_from_chat(chat_id=chat_id, from_user_id=from_user.get("id"))
    if account is not None:
        from apps.telegram.file_services import process_task_file_upload

        if process_task_file_upload(chat_id=chat_id, account=account, message=message):
            return

    if text.startswith("/start"):
        parts = text.split(maxsplit=1)
        token = parts[1].strip() if len(parts) > 1 else ""
        if token:
            link_account_by_token(token=token, chat_id=chat_id, username=username)
            return
        send_telegram_message(
            chat_id=chat_id,
            text=(
                "Привет! Чтобы получать задачи, откройте персональную ссылку "
                "из админки (поле «bot link») и нажмите Start.\n\n"
                f"Ваш chat ID: `{chat_id}`\n"
                "Его можно вписать в админку вручную, если нужно."
            ),
            reply_markup=build_main_menu_keyboard(),
        )
        return

    if text.startswith("/myid"):
        send_telegram_message(
            chat_id=chat_id,
            text=f"Ваш Telegram chat ID: `{chat_id}`",
            reply_markup=build_main_menu_keyboard(),
        )
        return

    if text.startswith("/help") or text == MENU_HELP_BUTTON:
        send_help_message(chat_id=chat_id)
        return

    from apps.telegram.discussion_keyboards import DISCUSSION_STOP_BUTTON, MENU_DIALOGS_BUTTON
    from apps.telegram.discussion_services import (
        relay_discussion_message,
        show_discussions_menu,
        stop_discussion,
    )

    if text.startswith("/stop") or text == DISCUSSION_STOP_BUTTON:
        stop_discussion(chat_id=chat_id)
        return

    if text.startswith("/dialogs") or text == MENU_DIALOGS_BUTTON:
        account = _resolve_account_from_chat(chat_id=chat_id, from_user_id=from_user.get("id"))
        if account is None:
            send_telegram_message(
                chat_id=chat_id,
                text=(
                    "Сначала привяжите аккаунт через персональную ссылку из админки "
                    "или попросите администратора указать ваш chat ID."
                ),
            )
            return
        show_discussions_menu(chat_id=chat_id, account=account)
        return

    account = _resolve_account_from_chat(chat_id=chat_id, from_user_id=from_user.get("id"))
    if account is not None and relay_discussion_message(
        chat_id=chat_id,
        account=account,
        text=text,
    ):
        return

    if text.startswith("/tasks") or text == MENU_TASKS_BUTTON:
        account = _resolve_account_from_chat(chat_id=chat_id, from_user_id=from_user.get("id"))
        if account is None:
            send_telegram_message(
                chat_id=chat_id,
                text=(
                    "Сначала привяжите аккаунт через персональную ссылку из админки "
                    "или попросите администратора указать ваш chat ID."
                ),
            )
            return
        show_task_history(chat_id=chat_id, account=account)
        return


def process_callback_query(*, callback_query: dict[str, Any]) -> None:
    """Handle inline keyboard presses."""
    from apps.telegram.discussion_keyboards import parse_discussion_callback
    from apps.telegram.discussion_services import process_discussion_callback

    callback_id = callback_query.get("id")
    data = (callback_query.get("data") or "").strip()
    message = callback_query.get("message") or {}
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    message_id = message.get("message_id")

    if not callback_id or chat_id is None or message_id is None:
        return

    discussion_payload = parse_discussion_callback(data)
    if discussion_payload is not None:
        process_discussion_callback(
            callback_id=callback_id,
            chat_id=chat_id,
            message_id=message_id,
            callback_query=callback_query,
            payload=discussion_payload,
        )
        return

    history_payload = parse_history_callback(data)
    if history_payload is not None:
        process_history_callback(
            callback_id=callback_id,
            chat_id=chat_id,
            message_id=message_id,
            callback_query=callback_query,
            payload=history_payload,
        )
        return

    process_task_action_callback(
        callback_id=callback_id,
        chat_id=chat_id,
        message_id=message_id,
        callback_query=callback_query,
        data=data,
    )


def process_history_callback(
    *,
    callback_id: str,
    chat_id: int,
    message_id: int,
    callback_query: dict[str, Any],
    payload: dict[str, Any],
) -> None:
    """Handle inline keyboard presses in the task history menu."""
    from apps.tasks import selectors as task_selectors
    from apps.tasks import services as task_services
    from apps.tasks.choices import TaskStatus
    from apps.tasks.models import Task

    account = _resolve_account_from_chat(
        chat_id=chat_id,
        from_user_id=(callback_query.get("from") or {}).get("id"),
    )
    if account is None:
        _answer_callback(callback_id, "Сначала привяжите аккаунт через /start.")
        return

    kind = payload["kind"]
    if kind == "projects":
        show_project_list(
            chat_id=chat_id,
            account=account,
            page=payload["page"],
            message_id=message_id,
            allow_unassigned_fallback=False,
        )
        _answer_callback(callback_id, "Список проектов обновлён.")
        return

    if kind == "project_tasks":
        show_project_tasks(
            chat_id=chat_id,
            account=account,
            project_uuid=payload["project_uuid"],
            page=payload["page"],
            message_id=message_id,
        )
        _answer_callback(callback_id, "Список задач обновлён.")
        return

    task_uuid: UUID = payload["task_uuid"]
    page: int = payload["page"]

    try:
        task = task_selectors.get_task_by_uuid(task_uuid)
    except Task.DoesNotExist:
        _answer_callback(callback_id, "Задача не найдена.")
        return

    if task.assignee_id != account.user_id:
        _answer_callback(callback_id, "Эта задача назначена другому пользователю.")
        return

    if kind == "view":
        show_task_detail(
            chat_id=chat_id,
            account=account,
            task=task,
            page=page,
            message_id=message_id,
        )
        _answer_callback(callback_id, task.title)
        return

    if kind == "files":
        from apps.telegram.file_services import show_task_files

        show_task_files(
            chat_id=chat_id,
            task=task,
            page=page,
            message_id=message_id,
        )
        _answer_callback(callback_id, "Файлы задачи")
        return

    if kind == "upload":
        from apps.telegram.file_services import enter_upload_mode

        enter_upload_mode(
            chat_id=chat_id,
            task=task,
            page=page,
            message_id=message_id,
        )
        _answer_callback(callback_id, "Отправьте файл")
        return

    if kind != "action":
        _answer_callback(callback_id, "Неизвестная команда.")
        return

    status_map = {
        "in_progress": TaskStatus.IN_PROGRESS,
        "done": TaskStatus.DONE,
    }
    new_status = status_map.get(payload["action"])
    if new_status is None:
        _answer_callback(callback_id, "Действие недоступно.")
        return

    if task.status in {TaskStatus.DONE, TaskStatus.CANCELLED}:
        _answer_callback(callback_id, "Задача уже закрыта.")
        return

    if task.status == TaskStatus.IN_PROGRESS and payload["action"] == "in_progress":
        _answer_callback(callback_id, "Задача уже в работе.")
        return

    updated_task = task_services.update_task_status(
        task=task,
        status=new_status,
        actor=account.user,
    )
    show_task_detail(
        chat_id=chat_id,
        account=account,
        task=updated_task,
        page=page,
        message_id=message_id,
    )
    _answer_callback(callback_id, f"Статус: {updated_task.get_status_display()}")


def process_task_action_callback(
    *,
    callback_id: str,
    chat_id: int,
    message_id: int,
    callback_query: dict[str, Any],
    data: str,
) -> None:
    """Handle inline keyboard presses on task notification messages."""
    from apps.tasks import selectors as task_selectors
    from apps.tasks import services as task_services
    from apps.tasks.choices import TaskStatus
    from apps.tasks.models import Task

    parsed = parse_task_callback_data(data)
    if parsed is None:
        _answer_callback(callback_id, "Неизвестная команда.")
        return

    task_uuid, action = parsed
    status_map = {
        "in_progress": TaskStatus.IN_PROGRESS,
        "done": TaskStatus.DONE,
    }
    new_status = status_map.get(action)
    if new_status is None:
        _answer_callback(callback_id, "Действие недоступно.")
        return

    account = _resolve_account_from_chat(
        chat_id=chat_id,
        from_user_id=(callback_query.get("from") or {}).get("id"),
    )
    if account is None:
        _answer_callback(callback_id, "Сначала привяжите аккаунт через /start.")
        return

    try:
        task = task_selectors.get_task_by_uuid(task_uuid)
    except Task.DoesNotExist:
        _answer_callback(callback_id, "Задача не найдена.")
        return

    if task.assignee_id != account.user_id:
        _answer_callback(callback_id, "Эта задача назначена другому пользователю.")
        return

    if task.status in {TaskStatus.DONE, TaskStatus.CANCELLED}:
        _answer_callback(callback_id, "Задача уже закрыта.")
        return

    if task.status == TaskStatus.IN_PROGRESS and action == "in_progress":
        _answer_callback(callback_id, "Задача уже в работе.")
        return

    updated_task = task_services.update_task_status(
        task=task,
        status=new_status,
        actor=account.user,
    )
    logger.info(
        "Telegram button updated task status",
        extra={
            "task_uuid": str(updated_task.uuid),
            "status": updated_task.status,
            "chat_id": chat_id,
            "user_email": account.user.email,
        },
    )
    text = format_task_notification(task=updated_task)
    keyboard = build_task_keyboard(updated_task)
    markup = keyboard if keyboard is not None else {"inline_keyboard": []}

    try:
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=markup,
        )
    except TelegramDisabledError:
        logger.info("Skipped Telegram message edit because integration is disabled")
    except TelegramAPIError:
        logger.exception("Failed to edit Telegram task message")

    _answer_callback(callback_id, f"Статус: {updated_task.get_status_display()}")


def show_task_history(
    *,
    chat_id: int,
    account: TelegramAccount,
    page: int = 0,
    message_id: int | None = None,
) -> None:
    """Open the task history flow starting from project selection."""
    show_project_list(
        chat_id=chat_id,
        account=account,
        page=page,
        message_id=message_id,
    )


NO_PROJECTS_MESSAGE = (
    "На данный момент нет проектов, иди отдохни и пей чай :)"
)


def show_project_list(
    *,
    chat_id: int,
    account: TelegramAccount,
    page: int = 0,
    message_id: int | None = None,
    allow_unassigned_fallback: bool = True,
) -> None:
    """Send or edit a paginated list of projects for the user."""
    from apps.projects import selectors as project_selectors

    queryset = project_selectors.list_projects_for_assignee(assignee=account.user)
    total_count = queryset.count()
    has_unassigned = project_selectors.assignee_has_unassigned_tasks(assignee=account.user)
    unassigned_count = (
        project_selectors.count_unassigned_tasks(assignee=account.user)
        if has_unassigned
        else 0
    )

    if total_count == 0 and has_unassigned and allow_unassigned_fallback:
        show_project_tasks(
            chat_id=chat_id,
            account=account,
            project_uuid=None,
            page=0,
            message_id=message_id,
        )
        return

    if total_count == 0:
        text = (
            NO_PROJECTS_MESSAGE
            if not allow_unassigned_fallback
            else "📋 У вас пока нет задач."
        )
        markup: dict[str, Any] | None = None
    else:
        page = max(page, 0)
        total_pages = max(1, ceil(total_count / HISTORY_PAGE_SIZE))
        page = min(page, total_pages - 1)
        projects = list(queryset[page * HISTORY_PAGE_SIZE : (page + 1) * HISTORY_PAGE_SIZE])
        text = (
            "📋 Ваши проекты\n\n"
            "Сначала выберите проект, затем откроете задачу:"
        )
        markup = build_project_history_keyboard(
            projects=projects,
            page=page,
            total_count=total_count,
            include_unassigned=has_unassigned,
            unassigned_count=unassigned_count,
        )

    _send_or_edit_history_message(
        chat_id=chat_id,
        text=text,
        markup=markup,
        message_id=message_id,
        edit_error_message="Failed to edit Telegram project list message",
    )


def show_project_tasks(
    *,
    chat_id: int,
    account: TelegramAccount,
    project_uuid: UUID | None,
    page: int = 0,
    message_id: int | None = None,
) -> None:
    """Send or edit a paginated list of tasks inside the selected project."""
    from apps.projects import selectors as project_selectors
    from apps.projects.models import Project
    from apps.tasks import selectors as task_selectors

    project = None
    if project_uuid is not None:
        try:
            project = project_selectors.get_project_by_uuid(project_uuid=project_uuid)
        except Project.DoesNotExist:
            show_project_list(
                chat_id=chat_id,
                account=account,
                page=0,
                message_id=message_id,
            )
            return

    if project is None:
        queryset = task_selectors.list_tasks(
            assignee=account.user,
            unassigned_only=True,
        )
    else:
        queryset = task_selectors.list_tasks(assignee=account.user, project=project)

    total_count = queryset.count()
    label = project_label(project=project)
    if total_count == 0:
        text = f"📁 {label}\n\nВ этом проекте пока нет задач."
        markup = build_task_history_keyboard(
            tasks=[],
            page=0,
            total_count=0,
            project_uuid=project_uuid,
        )
    else:
        page = max(page, 0)
        total_pages = max(1, ceil(total_count / HISTORY_PAGE_SIZE))
        page = min(page, total_pages - 1)
        tasks = list(queryset[page * HISTORY_PAGE_SIZE : (page + 1) * HISTORY_PAGE_SIZE])
        text = (
            f"📁 {label}\n"
            f"Задач: {total_count} · страница {page + 1} из {total_pages}\n\n"
            "Выберите задачу:"
        )
        markup = build_task_history_keyboard(
            tasks=tasks,
            page=page,
            total_count=total_count,
            project_uuid=project_uuid,
        )

    _send_or_edit_history_message(
        chat_id=chat_id,
        text=text,
        markup=markup,
        message_id=message_id,
        edit_error_message="Failed to edit Telegram task history message",
    )


def _send_or_edit_history_message(
    *,
    chat_id: int,
    text: str,
    markup: dict[str, Any] | None,
    message_id: int | None,
    edit_error_message: str,
) -> None:
    """Send a new history message or edit an existing one."""
    if message_id is None:
        send_telegram_message(chat_id=chat_id, text=text, reply_markup=markup)
        return

    try:
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=markup,
        )
    except TelegramDisabledError:
        logger.info("Skipped Telegram history edit because integration is disabled")
    except TelegramAPIError:
        logger.exception(edit_error_message)


def show_task_detail(
    *,
    chat_id: int,
    account: TelegramAccount,
    task: Any,
    page: int,
    message_id: int | None = None,
) -> None:
    """Send or edit a detailed task card in the history menu."""
    from apps.files import selectors as file_selectors

    attachment_count = file_selectors.list_attachments_for_task(task=task).count()
    text = format_task_detail(task=task, attachment_count=attachment_count)
    markup = build_task_detail_keyboard(
        task=task,
        page=page,
        attachment_count=attachment_count,
    )

    if message_id is None:
        send_telegram_message(chat_id=chat_id, text=text, reply_markup=markup)
        return

    try:
        client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=markup,
        )
    except TelegramDisabledError:
        logger.info("Skipped Telegram detail edit because integration is disabled")
    except TelegramAPIError:
        logger.exception("Failed to edit Telegram task detail message")


def send_help_message(*, chat_id: int) -> None:
    """Send bot usage instructions with the main menu keyboard."""
    send_telegram_message(
        chat_id=chat_id,
        text=(
            "Этот бот отправляет задачи из внутренней системы студии.\n\n"
            "Кнопка «Мои задачи» — сначала проект, затем список задач и детали.\n"
            "Кнопка «Диалоги» — личные и групповые обсуждения по задачам.\n"
            "В активном диалоге можно добавить участника.\n"
            "В карточке задачи — просмотр и загрузка файлов.\n"
            "Под новой задачей есть кнопки «В работе» и «Готово».\n\n"
            "Команды:\n"
            "/tasks — задачи\n"
            "/dialogs — диалоги\n"
            "/stop — завершить активный диалог\n"
            "/myid — показать chat ID\n"
            "/start <ссылка> — привязать аккаунт"
        ),
        reply_markup=build_main_menu_keyboard(),
    )


def _resolve_account_from_chat(
    *,
    chat_id: int,
    from_user_id: int | None = None,
) -> TelegramAccount | None:
    """Return the linked Telegram account for an incoming chat."""
    account = telegram_selectors.get_telegram_account_by_chat_id(chat_id=chat_id)
    if account is None and from_user_id is not None:
        account = telegram_selectors.get_telegram_account_by_chat_id(chat_id=from_user_id)
    return account


def _answer_callback(callback_id: str, text: str) -> None:
    """Send a toast response for an inline button press."""
    try:
        client.answer_callback_query(callback_query_id=callback_id, text=text)
    except TelegramDisabledError:
        return
    except TelegramAPIError:
        logger.exception("Failed to answer Telegram callback query")


def format_task_notification(*, task: Any) -> str:
    """Build a Russian notification message for a task assignment."""
    from apps.tasks.choices import TaskStatus

    headers = {
        TaskStatus.TODO: "📋 Новая задача",
        TaskStatus.IN_PROGRESS: "🔄 Задача в работе",
        TaskStatus.DONE: "✅ Задача выполнена",
        TaskStatus.CANCELLED: "❌ Задача отменена",
    }
    lines = [
        headers.get(task.status, "📋 Задача"),
        "",
        f"Проект: {project_label(project=getattr(task, 'project', None))}",
        f"Название: {task.title}",
    ]
    if task.description:
        lines.extend(["", f"Описание: {task.description}"])
    if task.due_date:
        lines.append(f"Срок: {task.due_date.strftime('%d.%m.%Y')}")
    lines.append(f"Статус: {task.get_status_display()}")
    return "\n".join(lines)


def format_task_detail(*, task: Any, attachment_count: int = 0) -> str:
    """Build a detailed Russian task card for the history menu."""
    lines = [
        "📄 Задача",
        "",
        f"Проект: {project_label(project=getattr(task, 'project', None))}",
        f"Название: {task.title}",
    ]
    if task.description:
        lines.extend(["", "Что нужно сделать:", task.description])
    else:
        lines.extend(["", "Описание не указано."])
    if task.due_date:
        from apps.tasks.reminders import format_days_until_deadline

        deadline = format_days_until_deadline(due_date=task.due_date)
        due_label = task.due_date.strftime("%d.%m.%Y")
        lines.append(f"Срок: {due_label} · {deadline.label}")
    if attachment_count:
        lines.append(f"Файлов: {attachment_count}")
    lines.extend(
        [
            f"Статус: {task.get_status_display()}",
            f"Обновлено: {task.updated_at.strftime('%d.%m.%Y %H:%M')}",
        ]
    )
    return "\n".join(lines)


def notify_user_about_task(*, user: User, task: Any) -> bool:
    """Send a task notification to the assignee's Telegram chat."""
    account = getattr(user, "telegram_account", None)
    if account is None:
        account = TelegramAccount.objects.filter(user=user).first()
    if account is None or not account.is_ready_for_notifications:
        logger.info(
            "Skipped Telegram task notification",
            extra={"user_uuid": str(user.uuid), "task_uuid": str(task.uuid)},
        )
        return False

    text = format_task_notification(task=task)
    keyboard = build_task_keyboard(task)
    queue_telegram_message(chat_id=account.chat_id, text=text, reply_markup=keyboard)
    return True
