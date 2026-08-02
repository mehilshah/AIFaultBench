#!/usr/bin/env python3
"""Reproduce BrowserProfile's Windows-only default-downloads-path failure."""

from __future__ import annotations

import errno
from pathlib import Path, PureWindowsPath
from unittest.mock import patch
from uuid import UUID

import browser_use.browser.profile as profile_module


class WindowsDownloadsPath(type(Path())):
	"""A local adapter for the Win32 mkdir result of ``Path('/tmp/...')``.

	The reference runner is Linux, where pathlib cannot construct WindowsPath.
	This remains an execution of the checkout's validator: only the OS-specific
	Path object is adapted, and it verifies that its input has the bad Windows
	root-relative spelling before returning the native WinError 183 result.
	"""

	def __new__(cls, value: str):
		self = super().__new__(cls, value)
		self.windows_spelling = str(PureWindowsPath(value))
		return self

	def exists(self) -> bool:
		return False

	def mkdir(self, *, parents: bool = False, exist_ok: bool = False) -> None:
		assert parents and exist_ok
		assert self.windows_spelling == r'\tmp\browser-use-downloads-12345678'
		error = FileExistsError(errno.EEXIST, 'Cannot create a file when that file already exists', r'\tmp')
		error.winerror = 183
		raise error


def main() -> None:
	# The buggy code imports uuid inside the validator, so patch uuid.uuid4 at
	# its source to make the generated default path deterministic.
	with patch('uuid.uuid4', return_value=UUID('12345678-1234-5678-1234-567812345678')):
		with patch.object(profile_module, 'Path', WindowsDownloadsPath):
			try:
				profile_module.BrowserProfile()
			except FileExistsError as error:
				assert getattr(error, 'winerror', None) == 183
				assert error.filename == r'\tmp'
				print('OBSERVED BUG: FileExistsError [WinError 183] while creating \\tmp from hard-coded /tmp downloads path')
				raise SystemExit(1)

	raise AssertionError('expected Windows default-downloads-path failure was not raised')


if __name__ == '__main__':
	main()
