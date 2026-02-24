import logging
import asyncio
from collections import defaultdict
from typing import Callable, Awaitable, Any

from .event_bus import IEventBus
from .base_event import BaseEvent


logger = logging.getLogger(__name__)

class InMemoryEventBus(IEventBus):
    def __init__(self):
        self._handlers: dict[str, list[Callable[[BaseEvent], Awaitable[None]]]] = defaultdict(list)

    def subscribe(self, event_name: str, handler: Callable[[BaseEvent], Awaitable[None]]) -> None:
        self._handlers[event_name].append(handler)
        logger.debug(f"Subscribed '{handler.__class__.__name__}' to '{event_name}'")

    async def publish(self, event: BaseEvent) -> None:
        handlers = self._handlers.get(event.event_name, [])

        if not handlers:
            logger.warning(f"No handlers for '{event.event_name}'")
            return

        results = await asyncio.gather(
            *[h(event) for h in handlers],
            return_exceptions=True
        )

        for h, result in zip(handlers, results):
            if isinstance(result, Exception):
                logger.error(
                    f"Handler '{h.__class__.__name__}' "
                    f"failed for '{event.event_name}': {result}"
                )


event_bus = InMemoryEventBus()
