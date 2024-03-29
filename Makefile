.PHONY: format

format:
	poetry run python -m isort --profile black src
	poetry run python -m black src

check_release:
ifndef VERSION
	$(error VERSION is undefined)
endif

release: check_release
	git flow release start $(VERSION)
	sed -i 's/^version =.*/version = "$(VERSION)"/' pyproject.toml
	sed -i 's/^release =.*/release = "$(VERSION)"/' doc/source/conf.py
	git add pyproject.toml doc
	git commit -m "Bump version to $(VERSION)"
	git flow release finish -m "Release $(VERSION)" $(VERSION) > /dev/null
