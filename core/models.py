"""
Универсальные модели для системы генерации кода
"""

import uuid
from typing import List, Literal
from uuid import UUID

from pydantic import BaseModel, Field


# Модель для элемента меню задач (структура {id, intent, task})
class TaskMenuItem(BaseModel):
    id: int = Field(description="Task ID/number")
    intent: str = Field(description="Brief task intention (2-4 words)")
    task: str = Field(description="Full task description")


# Модель для готового меню
class TaskMenu(BaseModel):
    id: str | UUID = Field(default_factory=lambda: uuid.uuid4())
    locale: Literal["en", "uk", "ru"] = Field(description="Menu language")
    title: str = Field(description="Menu title")
    items: List[TaskMenuItem] = Field(description="Menu items with id, intent, task")
    exit_option: str = Field(description="Exit option text")


# Модель для переводов интерфейса
class InterfaceMessages(BaseModel):
    id: str | UUID = Field(default_factory=lambda: uuid.uuid4())
    locale: Literal["en", "uk", "ru"] = Field(description="Messages language")
    input_prompt: str = Field(description="Input prompt text")
    goodbye: str = Field(description="Goodbye message")
    invalid_choice: str = Field(description="Invalid choice message")
    generating: str = Field(description="Generating message")
    generated_code_header: str = Field(description="Generated code header")
    save_prompt: str = Field(description="Save prompt text")
    saved_message: str = Field(description="Saved message")
    error_message: str = Field(description="Error message")


# Модель для сгенерированного кода
class GeneratedCode(BaseModel):
    id: str | UUID = Field(default_factory=lambda: uuid.uuid4())
    locale: Literal["en", "uk", "ru"] = Field(description="Code comments language")
    task_number: int = Field(description="Task number")
    task_description: str = Field(description="Original task description")
    code: str = Field(description="Clean Python code without markdown")


# Модель для файла заданий
class TaskFile(BaseModel):
    id: int = Field(description="File ID for selection")
    filename: str = Field(description="Filename without path")
    filepath: str = Field(description="Full path to file")
    description: str = Field(description="Brief description of file content")


# Модель для меню выбора файлов
class TaskFileMenu(BaseModel):
    id: str | UUID = Field(default_factory=lambda: uuid.uuid4())
    title: str = Field(description="Menu title")
    files: List[TaskFile] = Field(description="Available task files")
    exit_option: str = Field(description="Exit option text")


# Модель для конфигурации агента
class AgentConfig(BaseModel):
    task_file_path: str = Field(description="Path to task file")
    output_directory: str = Field(
        default="generated_code", description="Output directory for generated code"
    )
    tasks_directory: str = Field(
        default="tasks", description="Directory containing task files"
    )
    default_language: Literal["en", "uk", "ru"] = Field(
        default="en", description="Default interface language"
    )
    ai_model: str = Field(default="qwen-3-235b", description="AI model to use")
    provider: str = Field(default="PollinationsAI", description="AI provider to use")


# Модель для результата генерации
class GenerationResult(BaseModel):
    success: bool = Field(description="Whether generation was successful")
    task_id: int = Field(description="Task ID that was processed")
    file_path: str | None = Field(description="Path to generated file")
    error_message: str | None = Field(description="Error message if failed")
    code_preview: str | None = Field(description="Preview of generated code")
