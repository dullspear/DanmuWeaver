fetch("/result")
  .then((res) => res.json())
  .then(renderPlayer);

function renderPlayer(result) {
  const videoUrl = "/media";
  const dp = new DPlayer({
    container: document.getElementById("dplayer"),
    video: { url: videoUrl },
    // DPlayer 的弹幕加载永远走 apiBackend.read()，这里自定义成直接回调本地已算好的弹幕数组，不发真实网络请求
    apiBackend: {
      read: (options) => options.success(result.comments),
      send: (options) => options.success && options.success(),
    },
    danmaku: {
      id: "local",
      api: "local", // 占位：load() 内部会访问 this.options.api.maximum，自定义 apiBackend 不会真用这个值发请求，但字段必须存在
    },
  });

  // 等 DPlayer 把自己的 DOM 模板渲染完，再把缺失片段叠加进原生进度条(.dplayer-bar)里，不单独起一条
  dp.on("loadedmetadata", () => {
    const bar = dp.container.querySelector(".dplayer-bar");
    if (!bar) return;
    result.missing_segments.forEach((seg) => {
      const div = document.createElement("div");
      div.className = "missing-segment";
      div.style.left = `${(seg.start / result.long_duration) * 100}%`;
      div.style.width = `${((seg.end - seg.start) / result.long_duration) * 100}%`;
      div.title = `${seg.start}s ~ ${seg.end}s (short 中没有)`;
      bar.appendChild(div);
    });
  });
}
