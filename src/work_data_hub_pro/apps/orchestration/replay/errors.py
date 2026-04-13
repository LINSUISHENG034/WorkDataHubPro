from __future__ import annotations

from typing import Any


class ReplaySetupError(Exception):
    def __init__(
        self,
        *,
        domain: str,
        stage: str,
        message: str,
        context: dict[str, object],
        original_exception_type: str,
        original_exception_message: str,
    ) -> None:
        super().__init__(message)
        self.domain = domain
        self.stage = stage
        self.message = message
        self.context = dict(context)
        self.original_exception_type = original_exception_type
        self.original_exception_message = original_exception_message


class ReplayAssetNotFoundError(ReplaySetupError):
    pass


class ReplayConfigurationError(ReplaySetupError):
    pass


class ReplayContractSetupError(ReplaySetupError):
    pass


class ReplayDiagnosticsNotFoundError(ReplaySetupError):
    pass


def translate_replay_setup_error(
    domain: str,
    stage: str,
    exc: Exception,
    context: dict[str, object],
) -> ReplaySetupError:
    if isinstance(exc, ReplaySetupError):
        return exc

    original_exception_type = type(exc).__name__
    original_exception_message = str(exc)
    message = (
        f"{domain} replay setup failed during {stage}: "
        f"{original_exception_type}: {original_exception_message}"
    )
    error_cls: type[ReplaySetupError]

    if isinstance(exc, FileNotFoundError):
        if "diagnostic" in stage or "comparison_run_id" in context:
            error_cls = ReplayDiagnosticsNotFoundError
        else:
            error_cls = ReplayAssetNotFoundError
    elif isinstance(exc, (TypeError, KeyError)):
        error_cls = ReplayConfigurationError
    elif isinstance(exc, ValueError):
        error_cls = ReplayContractSetupError
    else:
        error_cls = ReplaySetupError

    return error_cls(
        domain=domain,
        stage=stage,
        message=message,
        context=context,
        original_exception_type=original_exception_type,
        original_exception_message=original_exception_message,
    )


__all__ = [
    "ReplayAssetNotFoundError",
    "ReplayConfigurationError",
    "ReplayContractSetupError",
    "ReplayDiagnosticsNotFoundError",
    "ReplaySetupError",
    "translate_replay_setup_error",
]
