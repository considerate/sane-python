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
    in
    {
      devShells = {
        default = pkgs.sane-python.env;
      };
    });
}
