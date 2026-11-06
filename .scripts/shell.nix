{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.texlive.combined.scheme-full  # Full LaTeX distribution with latexmk
    (pkgs.python3.withPackages (ps: [ ps.matplotlib ps.pillow ps.numpy ]))
  ];

  shellHook = ''
    echo "Run .scripts/generate_pdf.sh to build pdf/Stardust-NEXT-Podrecznik.pdf"
  '';
}
