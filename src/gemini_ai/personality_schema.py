"""Schema Pydantic pour les fichiers de personnalités."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, validator


class PersonalityTriggersConfig(BaseModel):
    """Décrit les triggers personnalisés d'une personnalité."""

    keywords: List[str] = Field(default_factory=list)
    commands: List[str] = Field(default_factory=list)

    @validator("keywords", "commands", each_item=True)
    def _strip_items(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError(
                "Les valeurs vides ne sont pas autorisées dans les triggers"
            )
        return cleaned


class PersonalityConfig(BaseModel):
    """Structure attendue pour les fichiers JSON de personnalités."""

    schema_version: int = Field(1, ge=1)
    name: str = Field(..., min_length=3)
    cultural_figure: str = Field(..., min_length=3)
    description: str = Field(..., min_length=10)
    iconic_phrases: List[str] = Field(...)
    emoji: str = Field("🎭", min_length=1)
    color: Optional[str] = Field(default=None, min_length=3)
    tone: Optional[str] = Field(default=None, min_length=3)
    signature: Optional[str] = Field(default=None, min_length=3)
    announcement_variants: Optional[List[str]] = Field(default=None)
    triggers: PersonalityTriggersConfig = Field(
        default_factory=PersonalityTriggersConfig
    )
    cooldown_override: Optional[int] = Field(default=None, ge=30, le=3600)
    sample_prompts: List[str] = Field(default_factory=list)

    @validator("iconic_phrases")
    def _validate_phrases(cls, value: List[str]) -> List[str]:
        if not value:
            raise ValueError("Au moins une phrase iconique est requise")
        cleaned = []
        for phrase in value:
            phrase_clean = phrase.strip()
            if len(phrase_clean) < 3:
                raise ValueError(
                    "Les phrases iconiques doivent contenir au moins 3 caractères"
                )
            cleaned.append(phrase_clean)
        return cleaned

    @validator("announcement_variants")
    def _validate_announcements(cls, value: Optional[List[str]]) -> Optional[List[str]]:
        if value is None:
            return None
        cleaned = [item.strip() for item in value if item.strip()]
        if value and not cleaned:
            raise ValueError(
                "Les annonces ne peuvent pas être uniquement composées d'espaces"
            )
        return cleaned or None

    @validator("sample_prompts")
    def _validate_sample_prompts(cls, value: List[str]) -> List[str]:
        return [item.strip() for item in value if item.strip()]
