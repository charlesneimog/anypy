import pytest
import os

import anytype
from anytype import Anytype
from pathlib import Path

any = Anytype()
any.auth()


def get_apispace() -> anytype.Space:
    spaces = any.get_spaces()
    for space in spaces:
        if space.name == "API":
            return space
    raise Exception("Space not found")


def test_create_space():
    space = get_apispace()
    if not space:
        any.create_space("API")
    assert get_apispace()


def test_get_spaces():
    spaces = any.get_spaces()
    assert len(spaces) > 0
    found_space = False
    for space in spaces:
        if space.name == "API":
            found_space = True
            break
    assert found_space


def test_template():
    # this is unsued yet, but just to keep testing
    template = anytype.Template()
    print(template)


def test_releation():
    # this is unsued yet, but just to keep testing
    relation = anytype.Relation()
    print(relation)


def test_block():
    # this is unsued yet, but just to keep testing
    block = anytype.Block()
    print(block)


def test_spacemethods():
    space = any.get_spaces()[0]
    objects = space.get_objects()
    obj = objects[0]
    obj = space.get_object(obj.id)


def test_createobj():
    space = get_apispace()
    if not space:
        raise Exception("Space not found")

    obj = anytype.Object()
    obj.name = "Hello World!"
    obj.icon = "🐍"
    obj.body = "`print('Hello World!')`"
    obj.description = "This is an object created from Python Api"
    objtype = space.get_type("Page")

    created_obj = space.create_object(obj, objtype)

    # Add assertions to verify the object was created
    assert created_obj.name == "Hello World!"
    assert created_obj.icon == "🐍"
    assert created_obj.body == "`print('Hello World!')`"
    assert (
        created_obj.description == "This is an object created from Python Api"
    )
    created_obj.add_title1("Test!")
    created_obj.add_title2("Test!")
    created_obj.add_title3("Test!")
    created_obj.add_codeblock("print('Hello World!')")
    created_obj.add_bullet("Hello World!")
    created_obj.add_checkbox("Hello World!")

    created_obj.delete()


def test_exportobj():
    space = get_apispace()
    if not space:
        raise Exception("Space not found")
    objs = space.get_objects()
    obj = objs[0]
    assert len(objs) > 0
    obj.export("export")

    # Handle the case for Linux / Flatpak
    if not Path("export").exists() and os.name == "posix":
        pytest.skip("Export test is not supported on flatpak for Linux.")
    else:
        assert Path("export").exists()
