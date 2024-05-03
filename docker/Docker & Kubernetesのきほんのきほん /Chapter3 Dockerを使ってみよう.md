## Dockerを使うには

以下3通り

- LinuxのマシンでDockerを使う
- 仮想マシンやレンタル環境にDockerを入れて、WindowsやMacで操作する
- Windows用やMac用のDockerを使う

### Windows用やMac用のDockerを使う

- 仮想環境の上にDockerの環境を構築するのと、デスクトップ版での仮想化環境とは若干仕組みが異なる
    - 仮想環境の上にDockerの環境を構築する
        - ユーザーが明示的に仮想化環境をインストールして操作する
        - 物理的なマシン→ OS → 仮想化環境 → LinuxOS → DockerEngineを置く
    - デスクトップ版での仮想化環境
        - → ユーザーが意識せずに仮想化環境を使用する
        - 物理艇なマシン → 仮想化環境 → LinuxOS → DockerEngineを置く
        
                                          → OS