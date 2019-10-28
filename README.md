# shape_2gt_pullery

python program to create svg file of pullery for 2gt timming belt

2GTタイミングペルト用歯付きプーリーの形状のSVGファイルを出力する
プログラム。

## インストール

このレポジトリをclone

    $ git clone https://github.com/h-nari/shape_2gt_pullery.git

pyclipperをインストール

    $ pip3 install pyclipper


## 使用方法

    $ python3 shape_2gt_pulley.py [options] 歯数

### 引数

#### 歯数    

整数、生成するプーリーの歯数。
小さすぎると、正常な形状が生成されない可能性もある。

### オプション

#### ```-o```,```--outfile``` *filename* 

出力するsvgファイル名を指定。
デフォルトは ',2gt_%d.svg'。
%dの部分には歯数の整数値が入る。

### ```-n```,```--noBezier```

ベジェ曲線化を行わない

### ```-e```,```--bezierError```

ベジェ曲線化の際の許容する誤差。
単位[mm], デフォルト 0.05

#### ```--dpi``` *float_value*

svgの座標の単位ピクセルを
現実の寸法に合わせるための
dpi(dot per inch)値。デフォルトは96。

#### ```-d```, ```--div``` *n*

プーリーの歯型を生成する際、
1歯あたり何回ベルト形状を回転させ
論理演算を行うかの値。
デフォルト4。

#### ```--calc_scale``` *float_value*

ポリゴン論理演算ライブラリpyclipperが
整数の座標しか受け付けないため、
元々の座標を何倍して pyclipperにわたすかの
値。デフォルトは10000。

## 変更履歴

### v1.0 - 2019/10/28(Mon)

* Bezier化
* 都合により --offset オプション廃止、将来復活予定

### v0.0 - 2019/10/17(thr)

* ファーストリリース
