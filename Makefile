VERSION = "v0.1.0"

help:	## Show all Makefile targets.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'

build: site.brutt.sittytalky.json ## build and install the application for testing
	@flatpak-builder --force-clean --user --install .build site.brutt.sittytalky.json

run: site.brutt.sittytalky.json build  ## run the application after build
	@flatpak run site.brutt.sittytalky

remove: site.brutt.sittytalky.json  ## remove application from system
	@flatpak uninstall site.brutt.sittytalky

bundle:	build ## create bundle for the applicatoin
	@flatpak run org.flatpak.Builder --force-clean --sandbox --user --install --ccache --repo=repo .build site.brutt.sittytalky.json
	@echo -e "\nGenerating Bundle .."
	@flatpak build-bundle repo site.brutt.sittytalky-$(VERSION)-x86_64_linux.flatpak site.brutt.sittytalky --runtime-repo=https://flathub.org/repo/flathub.flatpakrepo
