from abc import ABC, abstractmethod
from typing import Callable, Awaitable

from ..events.base_event import BaseEvent


class IEventBus(ABC):
    @abstractmethod
    def subscribe(
        self,
        event_name: str,
        handler: Callable[[BaseEvent], Awaitable[None]]
    ) -> None: ...

    @abstractmethod
    async def publish(self, event: BaseEvent) -> None: ...

