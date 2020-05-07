# python watchdog multiprocessing

watchdog의 observer을 병렬로 여러개 띄워 비동기적으로 처리하도록 작성한것입니다. 

감시할 디렉토리 리스트와, 이벤트 발생시 처리할 핸들러를 작성하시면 

서로 다른 디렉토리에 이벤트 동시발생시 서로다른 동작을 병렬적으로 수행합니다. 

부하를 줄이고 속도향상을 위해 connection pool도 적용해보았습니다.
