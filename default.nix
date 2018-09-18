with import <nixpkgs> {};

stdenv.mkDerivation rec {
  name = "env";

  env = buildEnv { name = name; paths = buildInputs; };
  
  buildInputs = [
    (python36.buildEnv.override {
        ignoreCollisions = true;
        extraLibs = with python36Packages; [
	    requests
            statsmodels
        ];
    })
  ];
}
