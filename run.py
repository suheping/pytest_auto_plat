import pytest
print('123')
pytest.main(["--reruns", "1", "--reruns-delay",
             "2", "--alluredir", "result"])
