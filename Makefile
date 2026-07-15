# Convenience wrappers around ./bin/pytrain, for when you just want to practise
# and not think about the command surface.
#
# New to the material?  Let it teach you first:
#
#     make learn     # explains the next task, then sets up its workspace to try
#     $EDITOR workspace/<domain>/<task>/solution.py
#     make check     # grade it   (then `make learn` again for the next one)
#
# Already know the ropes?  Just practise:
#
#     make train     # picks what you should do next (new material or a review)
#     make check     # grade the task you're on
#
# `make train` decides on its own whether to give you new material (in a
# fundamentals-first order) or bring back something older for a spaced-
# repetition review. Everything here just forwards to ./bin/pytrain — run
# `make help` for the list, or `./bin/pytrain help` for the full CLI
# (start/reset/solution and per-task ids).

PYTRAIN := ./bin/pytrain
.DEFAULT_GOAL := help

.PHONY: help learn train next check solution list status cli

help: ; @printf 'pytrain — just run one of:\n\n  make learn      teach the next task, then set up its workspace to try\n  make train      pick the next task for you (new material, or a review)\n  make check      grade the task you are currently on\n  make solution   reveal the reference solution for it\n  make list       every task, grouped by domain, with your status\n  make status     your XP, streak and per-domain completion\n\nFull CLI (start/reset a specific task by id):  $(PYTRAIN) help\n'

learn:    ; @$(PYTRAIN) learn
train:    ; @$(PYTRAIN) train
next:     ; @$(PYTRAIN) train
check:    ; @$(PYTRAIN) check
solution: ; @$(PYTRAIN) solution
list:     ; @$(PYTRAIN) list
status:   ; @$(PYTRAIN) status
cli:      ; @$(PYTRAIN) help
