
help:	## Show all Makefile targets.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'

build: site.brutt.sittytalky.json ## build and install the application for testing
	@flatpak-builder --force-clean --user --install .build site.brutt.sittytalky.json

run: site.brutt.sittytalky.json build  ## run the application after build
	@flatpak run site.brutt.sittytalky

remove: site.brutt.sittytalky.json  ## remove application from system
	@flatpak uninstall site.brutt.sittytalky
