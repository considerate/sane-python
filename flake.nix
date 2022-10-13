{
  inputs = {
    nixpkgs = {
      url = "github:NixOS/nixpkgs";
    };
    flake-utils = {
      url = "github:numtide/flake-utils";
    };
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
    };
  };
  outputs = inputs: inputs.flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import inputs.nixpkgs {
        inherit system;
        overlays = [
          inputs.poetry2nix.overlay
          (final: prev: {
            sane-python = final.poetry2nix.mkPoetryApplication {
              projectDir = ./.;
              overrides = final.poetry2nix.overrides.withDefaults (self: super: {
                flit-scm = self.callPackage ./flit-scm.nix { };
                exceptiongroup = super.exceptiongroup.overridePythonAttrs (old: {
                  nativeBuildInputs = old.nativeBuildInputs ++ [
                    self.flit-scm
                  ];
                });
              });
            };
          })
        ];
      };
      flake = {
        packages = {
          default = pkgs.sane-python;
        };
        legacyPackages = pkgs;
        devShells = {
          default = pkgs.sane-python.overrideAttrs (old: {
            nativeBuildInputs = (old.nativeBuildInputs or [ ]) ++ [
              pkgs.sane-python.python.pkgs.poetry
              pkgs.sane-python.python.pkgs.black
              pkgs.sane-python.python.pkgs.flake8
              pkgs.python-language-server
            ];
          });
        };
        devShell = flake.devShells.default;
      };
    in
    flake);
}
