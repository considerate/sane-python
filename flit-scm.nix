{ buildPythonPackage
, fetchPypi
, flit-core
, flitBuildHook
, setuptools-scm
}:
buildPythonPackage {
  pname = "flit-scm";
  version = "1.7.0";
  format = "flit";
  src = fetchPypi {
    pname = "flit_scm";
    version = "1.7.0";
    sha256 = "961bd6fb24f31bba75333c234145fff88e6de0a90fc0f7e5e7c79deca69f6bb2";
  };
  nativeBuildInputs = [
    flit-core
    flitBuildHook
    setuptools-scm
  ];
  pythonImportsCheck = [ "flit_scm" ];
}
