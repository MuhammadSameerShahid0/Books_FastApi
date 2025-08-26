from abc import ABC, abstractmethod
from typing import Dict, Any
from Schema.Google2FASchema import Google2FAResponse


class IGoogle2FAService(ABC):

    @abstractmethod
    def enable_2FA(self, email: str) -> Google2FAResponse:
        pass

    @abstractmethod
    def google_enable_2fa(self, email: str) -> Google2FAResponse:
        pass

    @abstractmethod
    def google_disable_2fa(self, email: str) -> Dict[str, str]:
        pass

    @abstractmethod
    def disable_2fa(self, email: str) -> Dict[str, str]:
        pass