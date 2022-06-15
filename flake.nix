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
            sane-python = final.poetry2nix.mkPoetryEnv {
              projectDir = ./.;
            };
          })
        ];
      };
      flake = {
        devShells = {
          default = pkgs.sane-python.env.overrideAttrs (old: {
            nativeBuildInputs = (old.nativeBuildInputs or [ ]) ++ [
              pkgs.sane-python.python.pkgs.poetry
            ];
          });
        };
        devShell = flake.devShells.default;
      };
    in
    flake);
}
