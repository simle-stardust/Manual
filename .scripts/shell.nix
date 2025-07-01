{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.pandoc
    pkgs.texlive.combined.scheme-full  # Provides a full LaTeX distribution
  ];

  shellHook = ''
    echo "Nix shell for Pandoc and TeX Live is active."
    echo "You can now use 'pandoc' to convert your Markdown files."
  '';
}