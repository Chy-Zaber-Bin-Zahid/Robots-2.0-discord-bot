{ pkgs }: {
  deps = [
    pkgs.sudo
    pkgs.nodejs-16_x
    pkgs.python38Full
    pkgs.replitPackages.prybar-python3
    pkgs.ffmpeg
  ];
  env = rec {
    LD_PRELOAD = "${pkgs.libopus}/lib/libopus.so";
    PYTHONBIN = "${pkgs.python38Full}/bin/python3.8";
    LANG = "en_US.UTF-8";
  };
}
