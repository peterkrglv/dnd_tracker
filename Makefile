include Makefile.campaign
include Makefile.character
include Makefile.chat
include Makefile.dice
include Makefile.export
include Makefile.handbook
include Makefile.setting
include Makefile.user 

format: campaign-format character-format chat-format dice-format export-format handbook-format setting-format user-format

check: campaign-check character-check chat-check dice-check export-check handbook-check setting-check user-check

mr: format check

