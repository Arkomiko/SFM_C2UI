# Code

Engine source code.

Everything public about these modules is declared in `Core/API`; App, the tools
and plugins import that contract, never these modules directly. That is what
lets the engine change without breaking anything built on it.
