import time
import uuid

from google.adk.events import Event, EventActions
from veadk.memory import ShortTermMemory

short_term_memory = ShortTermMemory(
    backend="sqlite",
)
APP_NAME = "test_app"
USER_ID = "test_user"
SESSION_ID = "test_session"


async def update_session_state(state_changes: dict):
    # 获取session
    session = await short_term_memory.session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    if session is None:
        session = await short_term_memory.session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID,
        )

    # --- Create Event with Actions ---
    actions_with_update = EventActions(state_delta=state_changes)  # 表示修改state的动作
    # This event might represent an internal system action, not just an agent response
    system_event = Event(
        invocation_id="inv_login_update",
        author="system",  # Or 'agent', 'tool' etc.
        actions=actions_with_update,
        timestamp=time.time(),
        # content might be None or represent the action taken
    )

    # --- Append the Event (This updates the state) ---
    await short_term_memory.session_service.append_event(session, system_event)
    print("`append_event` called with explicit state delta.")


async def check_session_state():
    # --- Check Updated State ---
    updated_session = await short_term_memory.session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    print(f"State event: {updated_session.state}")


if __name__ == "__main__":
    import asyncio

    # 查看修改之前的状态
    asyncio.run(check_session_state())

    asyncio.run(
        update_session_state(
            {
                "uuid": uuid.uuid4().hex,
            }
        )
    )

    # 检查修改之后的状态
    asyncio.run(check_session_state())
