from script_share import Script, ScriptExecutor

def test_upload_script():
    executor = ScriptExecutor()
    script = Script("test_script", "print('Hello World')", ["library1"])
    executor.upload_script(script)
    assert script.name in executor.scripts

def test_execute_script():
    executor = ScriptExecutor()
    script = Script("test_script", "print('Hello World')", ["library1"])
    executor.upload_script(script)
    output = executor.execute_script("test_script")
    assert output == "Executed test_script with libraries ['library1']"

def test_get_libraries():
    executor = ScriptExecutor()
    libraries = executor.get_libraries()
    assert libraries == ["library1", "library2", "library3"]

def test_execute_script_not_found():
    executor = ScriptExecutor()
    try:
        executor.execute_script("non_existent_script")
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == "Script not found"
