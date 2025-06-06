from typing import Any, AsyncIterator, Dict, List, Optional

from g4f.Provider import Free2GPT, PollinationsAI


class FixedPollinationsAI(PollinationsAI):
    """
    Исправленная версия PollinationsAI, которая решает проблему с 'NoneType' object has no attribute 'update'
    Специально адаптирована для работы с pydantic_ai
    """

    @staticmethod
    def _ensure_extra_body(kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Обеспечивает корректное состояние extra_body в kwargs"""
        if "extra_body" not in kwargs or kwargs["extra_body"] is None:
            kwargs["extra_body"] = {}
        elif not isinstance(kwargs["extra_body"], dict):
            kwargs["extra_body"] = {}

        return kwargs

    @staticmethod
    def _create_error_response(error_msg: str) -> Dict[str, Any]:
        """Создает стандартный ответ об ошибке"""
        return {
            "choices": [
                {
                    "message": {"content": f"Ошибка: {error_msg}"},
                    "finish_reason": "error",
                }
            ],
            "model": "pollinations-ai",
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        }

    @classmethod
    async def _generate_text(
        cls,
        model: str,
        messages: List[Dict[str, str]],
        proxy: Optional[str] = None,
        **kwargs,
    ) -> AsyncIterator[str]:
        """
        Исправленная версия метода _generate_text с защитой от ошибки extra_body.update()
        """
        try:
            kwargs = cls._ensure_extra_body(kwargs)

            async for chunk in super()._generate_text(
                model, messages, proxy=proxy, **kwargs
            ):
                yield chunk

        except AttributeError as e:
            if "'NoneType' object has no attribute 'update'" in str(e):
                kwargs = cls._ensure_extra_body(kwargs)
                try:
                    async for chunk in super()._generate_text(
                        model, messages, proxy=proxy, **kwargs
                    ):
                        yield chunk
                except Exception as retry_error:
                    yield f"Ошибка генерации текста: {str(retry_error)}"
            else:
                yield f"Ошибка атрибута: {str(e)}"

        except Exception as e:
            yield f"Ошибка провайдера: {str(e)}"

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: List[Dict[str, str]],
        proxy: Optional[str] = None,
        **kwargs,
    ) -> AsyncIterator[str]:
        """
        Исправленная версия create_async_generator
        """
        try:
            kwargs = cls._ensure_extra_body(kwargs)

            async for chunk in super().create_async_generator(
                model, messages, proxy=proxy, **kwargs
            ):
                yield chunk

        except AttributeError as e:
            if "'NoneType' object has no attribute 'update'" in str(e):
                kwargs = cls._ensure_extra_body(kwargs)
                try:
                    async for chunk in super().create_async_generator(
                        model, messages, proxy=proxy, **kwargs
                    ):
                        yield chunk
                except Exception as retry_error:
                    yield f"Ошибка генерации: {str(retry_error)}"
            else:
                yield f"Ошибка: {str(e)}"

        except Exception as e:
            yield f"Ошибка: {str(e)}"

    @classmethod
    def create_completion(
        cls, model: str, messages: List[Dict[str, str]], stream: bool = False, **kwargs
    ) -> Any:
        """
        Основной метод create_completion с исправлениями для совместимости с pydantic_ai
        """
        try:
            kwargs = cls._ensure_extra_body(kwargs)

            result = super().create_completion(model, messages, stream=stream, **kwargs)
            return result

        except AttributeError as e:
            if "'NoneType' object has no attribute 'update'" in str(e):
                kwargs = cls._ensure_extra_body(kwargs)
                try:
                    result = super().create_completion(
                        model, messages, stream=stream, **kwargs
                    )
                    return result
                except Exception as retry_error:
                    return cls._create_error_response(
                        f"Ошибка генерации: {str(retry_error)}"
                    )
            else:
                return cls._create_error_response(f"Ошибка атрибута: {str(e)}")

        except Exception as e:
            return cls._create_error_response(f"Ошибка провайдера: {str(e)}")


__all__ = ["FixedPollinationsAI"]
