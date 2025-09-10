from abc import ABC, abstractmethod


class IEmailService(ABC):
    
    @abstractmethod
    async def send_email(self, user_email: str, subject: str, body: str):
        pass

    async def email_code(self) -> int:
        pass

    async def login_template(self, verification_code: int, name: str) -> str:
        pass