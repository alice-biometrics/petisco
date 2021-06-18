class RabbitMqExchangeNameFormatter:
    @staticmethod
    def retry(exchange_name: str) -> str:
        return f"retry.{exchange_name}"

    @staticmethod
    def dead_letter(exchange_name: str) -> str:
        return f"dead_letter.{exchange_name}"
