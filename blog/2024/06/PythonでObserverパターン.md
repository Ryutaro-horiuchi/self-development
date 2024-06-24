# 初めに

# 前提

- 記事で触れること or 対象読者
    - オブジェクト指向に馴染みがある
    - クラス、インスタンス、継承、コンポジション、抽象などオブジェクト指向に関する基本的なことを知っている
    - Observerパターンについて知りたい or おさらいしておきたい

# 本題

## Observerパターンの概要

- あるクラスの変更を検知して、別のクラスに変更を適用したいときによく使用されるデザインパターンです。このデザインパターンでは、サブジェクトとオブザーバーの二つの役割で成り立っています。
- サブジェクトは状態の変化を通知したいオブジェクトであり、オブザーバーはサブジェクトからの変更通知を受け取りたいオブジェクトです。サブジェクトに更新があれば、オブザーバーもその変更を受けて、何かしらの処理を実施します。
- よくあるSNSシステムにはあるユーザーが投稿したときに、通知を受け取るようにする機能があると思いますが、サブジェクトとオブザーバーの関係は、これによく似ていると思います。
    
    (図で表現できたらよさそう?)
    

## クラス図

Observerパターンの基本的なクラス構成は以下になります

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/464f34c5-7cab-4436-9830-c8196459ac01/Untitled.png)

- Subject
    - Observerインスタンスをコンポジションとして持ちます。そのため、メソッドにObserverインスタンスを登録する`registerObserver(),` 反対に削除する`remoteObserver()`が用意されています
    - `notifyObservers()`はSubjectの状態の変化により、実際にObserverに変更を通知するメソッドになります。
- ConcreteSubject
    - Subjectの子クラスになります。
    - `getState()`、`setState()`はそれぞれオブザーバが監視したい**状態**を取得する、設定するメソッドになります。
- Observer, ConcreteObserver
    - Observerは抽象クラス、ConcreteObserverは具象クラスになります。
    - 変更通知を受け取るクラスであり、`update()`にて通知を受け取った際の処理を実行します

## 実例  気象観測システム

概要やクラス図を見てもイメージが湧きづらい部分もあると思うので、ここでは実際にコードを書いて、より理解を深めてみたいと思います。

以下の仕様を満たす「気象観測システム」を、Observerパターンで実装してみます

<aside>
💡 概要

- 気象観測システムは現在の気温を監視し、複数の通知方法を通じてユーザーに最新の気温情報を提供する
</aside>

<aside>
💡 要件

- システムは現在の気温を取得し、設定する
- 気温が更新された際に、以下の処理を行う
    - 気温ディスプレイの更新
    - 登録ユーザーにメール送信をする
    - 管理しているウェブサイトに表示する
</aside>

### SubjectとObserverクラスの作成

まずはそれぞれの親クラスを作成します

- Observer
    
    ```python
    from abc import ABC, abstractmethod
    
    class Observer(ABC):
        @abstractmethod
        def update():
            pass
    ```
    
    - Pythonでは、abc.ABCクラスを継承することで、抽象クラスを定義することができます。abstractmethodをデコレーターとすることで抽象メソッドとし、更新処理を呼び出す際のインターフェースを定めています。
- Subject
    
    ```python
    class Subject():
        def __init__(self):
            self.observers = []
    
        def register_observer(self, observer: Observer):
            """オブザーバーを登録する"""
            if observer not in self.observers:
                self.observers.append(observer)
    
        def remove_observer(self, observer: Observer):
            """オブザーバーを削除する"""
            self.observers.remove(observer)
    
        def notify_observers(self):
            """オブザーバーに変更を通知する"""
            for observer in self.observers:
                observer.update()
    ```
    

### Subjectサブクラスの作成

現在の気象情報を観測するクラスがSubjectサブクラスの対象となります。

```python
class WeatherData(Subject):
    """気象観測クラス"""
    def __init__(self):
        super().__init__()
        self._temperature = 0

    def get_temperature(self):
        """気温を取得する"""
        return self._temperature

    def set_temperature(self, temperature: int):
        """新たな気温を設定する"""
        self._temperature = temperature
        self.notify_observers()
```

- Subjectクラスを継承します。監視対象となる気温が変更された際に、`notify_observers()`を呼び出し、対象のオブサーバークラスに変更を通知するようにします

### Observerサブクラスの作成

気温の変化があった際に処理をしたい3つの要件が、そのままObserverサブクラスの対象となります。

```python
class Display(Observer):
    """気温表示クラス"""
    def __init__(self, weather_data: WeatherData):
        self.weather_data = weather_data
        weather_data.register_observer(self)

    def update(self):
        """ディスプレイに表示している気温情報を更新する"""
        temperature = self.weather_data.get_temperature()
        print(f'ディスプレイをアップデート - 現在の気温は{temperature}°Cです')

class EmailNotifier(Observer):
    """メール通知クラス"""
    def __init__(self, weather_data: WeatherData):
        self._email_addresses = []
        self.weather_data = weather_data
        weather_data.register_observer(self)

    def update(self):
        """登録メールアドレスに気温情報を通知する"""
        temperature = self.weather_data.get_temperature()
        print(f'登録メールアドレスに新規気温情報 {temperature}°Cを通知しました')

class WebPortal(Observer):
    """気象情報webサイトクラス"""
    def __init__(self, weather_data: WeatherData):
        self.weather_data = weather_data
        weather_data.register_observer(self)

    def update(self):
        """ウェブサイトに気温情報を表示する"""
        temperature = self.weather_data.get_temperature()
        print(f'ウェブサイトをアップデート - 現在の気温は{temperature}°Cです')
```

では実際に使用してみましょう。気温を28度に設定してみます。

```python
if __name__ == "__main__":
		# 初期化
    weather_data = WeatherData()
    display = Display(weather_data)
    email_notifier = EmailNotifier(weather_data)
    web_portal = WebPortal(weather_data)

    # 気温を28度に設定
    weather_data.set_temperature(28)

#=> ディスプレイをアップデート - 現在の気温は28°Cです
#=> 登録メールアドレスに新規気温情報 28°Cを通知しました
#=> ウェブサイトをアップデート - 現在の気温は28°Cです
```

気温が更新された際に、それに伴うオブザーバーの更新処理も実行できていることが確認できます

新たにメール配信のみ通知の対象から外す要望が挙がったとします。その後気温を設定し直してみます

```python
if __name__ == "__main__":
		# 初期化
    weather_data = WeatherData()
    display = Display(weather_data)
    email_notifier = EmailNotifier(weather_data)
    web_portal = WebPortal(weather_data)

    # 気温を28度に設定
    weather_data.set_temperature(28)
    weather_data.remove_observer(email_notifier)
    print('-------メール通知をオブザーバーから外しました-------')

    # 気温を23度に設定
    weather_data.set_temperature(23)

#=> ディスプレイをアップデート - 現在の気温は28°Cです
#=> 登録メールアドレスに新規気温情報 28°Cを通知しました
#=> ウェブサイトをアップデート - 現在の気温は28°Cです

#=> -------メール通知をオブザーバーから外しました-------

#=> ディスプレイをアップデート - 現在の気温は23°Cです
#=> ウェブサイトをアップデート - 現在の気温は23°Cです
```

メール通知のみ、外し他の処理は影響なく実行されていることが確認できました