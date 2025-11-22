import modules.cpu_module as cpu_module
import modules.gpu_module as gpu_module
import modules.network_module as network_module
import modules.storage_module as storage_module


def test_cpu_module_connects():
    res = cpu_module.connect_cpu(intensity=1)
    assert isinstance(res, dict)
    assert res.get("success") is True


def test_gpu_module_connects():
    res = gpu_module.connect_gpu(intensity=1)
    assert isinstance(res, dict)
    assert res.get("success") is True


def test_network_module_connects_and_toggles():
    # network_module.connect_network is a UI-friendly toggle; calling it should return a dict
    res = network_module.connect_network(intensity=1)
    assert isinstance(res, dict)
    assert "message" in res


def test_storage_module_connects_fast():
    # Make storage module fast for test by reducing demo time
    # The module exposes `demoTime` global; set to 0 to skip heavy loop.
    storage_module.demoTime = 0
    res = storage_module.connect_storage(intensity=1)
    assert isinstance(res, dict)
    assert res.get("success") is True
