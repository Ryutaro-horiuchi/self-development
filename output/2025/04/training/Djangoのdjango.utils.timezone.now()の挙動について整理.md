## はじめに

- Djangoで用意されている`django.utils.timezone.now()`の挙動は`USE_TZ`の設定によって挙動が変わる
- 整理したいと思い、備忘録としてまとめておく

## 前提

- 検証環境
    - macOS Sequoia 15.4.1
    - Django 5.2
    - Python3.13
- TIME_ZONE
    - `Asia/Tokyo`で検証

## 本題

### USE_TZ = Trueの時

- 出力
    
    ```python
    >>> from django.utils import timezone
    >>> print(timezone.now())
    2025-04-27 22:45:28.485428+00:00
    ```
    
    - TIME_ZONEの設定に関係ないUTCの時刻を返す
    
    > [**`USE_TZ`**](https://docs.djangoproject.com/ja/5.1/ref/settings/#std-setting-USE_TZ) が **`True`** の場合、 UTC の現在時刻を表す [aware](https://docs.djangoproject.com/ja/5.1/topics/i18n/timezones/#naive-vs-aware-datetimes) な日時になります。 [**`now()`**](https://docs.djangoproject.com/ja/5.1/ref/utils/#django.utils.timezone.now) は常に [**`TIME_ZONE`**](https://docs.djangoproject.com/ja/5.1/ref/settings/#std-setting-TIME_ZONE) の値に関係なく UTC の時刻を返すことに注意してください
    > 
- テンプレート
    - views.py
        
        ```python
        from django.shortcuts import render
        from django.utils import timezone
        
        def timezone_test(request):
          now = timezone.now()
          return render(request, 'timezone.html', {'value': now})
        ```
        
    - timezone.html
        
        ```html
        {% load tz %}
        
        <div>
          {% localtime on %}
            <p>localtime on {{ value }}</p>
          {% endlocaltime %}
        
          {% localtime off %}
          <p>localtime off {{ value }}</p>
          {% endlocaltime %}
        
          <p>{{ value }}</p>
        </div>
        ```
        
        - localtimeを使用することで、カレントタイムゾーン(設定されていなければ、デフォルトタイムゾーン)に変換して出力することができる
    - レンダリング
        
        ![image.png](attachment:ea3ea666-d757-4601-a0d5-7869b7f10348:image.png)
        
        - localtimeを使用することで、UTCの時刻からデフォルトのタイムゾーンに変換して出力される。
            - 注: activateを使用すると、デフォルトではなくカレントタイムゾーンが使用されるとのこと([参考](https://www.notion.so/7426cd23c3e14717afec617ad90aef1b?pvs=21))。使用されていないと、デフォルト

### USE_TZ = Falseの時

- 出力
    
    ```python
    >>> from django.utils import timezone
    >>> timezone_now = timezone.now()
    >>> print(timezone_now)
    2025-04-28 07:14:47.608404
    ```
    
    - タイムゾーンを考慮しないローカルタイムが出力されている
        
        > [**`USE_TZ`**](https://docs.djangoproject.com/ja/5.1/ref/settings/#std-setting-USE_TZ) が **`False`** の場合、システムのローカルタイムゾーンで現在の時刻を表す、関連するタイムゾーンのない [naive](https://docs.djangoproject.com/ja/5.1/topics/i18n/timezones/#naive-vs-aware-datetimes) な日時（タイムゾーンの関連がない日時）になります。
        > 
- テンプレート
    - views.pyとtimezone.htmlは同じ
    - 出力
        
        ![image.png](attachment:8bd4e430-22e2-4ea9-853b-ddf10dd05131:image.png)
        
        localtimeの使用に関係なく常にローカルタイムが返されている
        

## まとめ

- USE_TZ=Trueの時は、常にUTCの時刻を返す。テンプレートに出力するときは、デフォルトタイムゾーンに変換される。(`activate()`を使用しているときは、カレントタイムゾーンに変換)
- USE_TZ=Falseの時は、常にローカルの時刻を返す。テンプレートに出力するときも同様

## 参考

- https://docs.djangoproject.com/ja/5.1/topics/i18n/timezones/#time-zone-aware-output-in-templates