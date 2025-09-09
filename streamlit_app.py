import os
import tempfile
from pathlib import Path

import streamlit as st
from openai import OpenAI
import yt_dlp
from moviepy.editor import VideoFileClip

# -------- 설정 --------
TRANSCRIBE_MODEL = "whisper-1"
SUMMARIZE_MODEL  = "gpt-4o-mini"
CHUNK_CHAR_LEN   = 6000
LANG_HINT        = None
# ----------------------

def get_client(api_key: str) -> OpenAI:
    return OpenAI(api_key=api_key)

def download_audio_from_youtube(url: str, outdir: Path) -> Path:
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(outdir / "ytdlp_temp"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "m4a",
            "preferredquality": "192",
        }],
        "quiet": True,
        "noprogress": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url, download=True)
        for f in outdir.glob("ytdlp_temp*.m4a"):
            return f
    raise RuntimeError("오디오 다운로드 실패")

def extract_audio(video_path: Path, out_audio: Path) -> Path:
    clip = VideoFileClip(str(video_path))
    tmp_wav = out_audio.with_suffix(".wav")
    clip.audio.write_audiofile(
        str(tmp_wav),
        fps=16000,
        nbytes=2,
        codec="pcm_s16le",
        ffmpeg_params=["-ac", "1"],
    )
    clip.close()
    return tmp_wav

def transcribe_audio(client: OpenAI, audio_path: Path) -> str:
    with open(audio_path, "rb") as f:
        resp = client.audio.transcriptions.create(
            model=TRANSCRIBE_MODEL,
            file=f,
            response_format="text",
            language=LANG_HINT,
        )
    return getattr(resp, "text", str(resp))

def chunk_text(text: str, chunk_size: int = CHUNK_CHAR_LEN):
    text = text.strip()
    chunks = []
    start = 0
    N = len(text)
    while start < N:
        end = min(start + chunk_size, N)
        if end < N:
            period = text.rfind(".", start, end)
            if period != -1 and period > start + chunk_size * 0.7:
                end = period + 1
        chunks.append(text[start:end].strip())
        start = end
    return chunks

def summarize_map(client: OpenAI, chunk: str, lang: str = "한국어") -> str:
    prompt = f"""당신은 뛰어난 요약가입니다.
아래 전사 텍스트를 {lang}로 핵심 bullet 5~8개로 요약하고, 중요한 숫자/고유명사를 보존하세요.

[전사]
{chunk}
"""
    resp = client.responses.create(
        model=SUMMARIZE_MODEL,
        input=[{"role": "user", "content": prompt}],
    )
    return resp.output_text

def summarize_reduce(client: OpenAI, bullets, lang: str = "한국어") -> str:
    joined = "\n\n---\n\n".join(bullets)
    prompt = f"""다음은 여러 덩어리에서 뽑은 핵심 bullet들입니다. 이를 통합해 최종 요약을 만들어 주세요.

요청사항:
- 5문장 '핵심 요약'
- 7~10개 bullet '상세 포인트'
- '실행 항목(있다면)' 3~5개
- 길이 300~500자 내외의 '짧은 요약'도 제공
- 결과는 {lang}로 작성

[부분 요약들]
{joined}
"""
    resp = client.responses.create(
        model=SUMMARIZE_MODEL,
        input=[{"role": "user", "content": prompt}],
    )
    return resp.output_text

# ---------------- Streamlit UI ----------------

st.set_page_config(page_title="🎬 영상 요약기", layout="wide")
st.title("🎬 영상 요약 AI")

# 🔑 API Key 입력은 Streamlit Cloud의 Secrets 기능 권장
api_key = st.text_input("🔑 OpenAI API Key", type="password")

src_type = st.radio("입력 방식 선택", ["유튜브 링크", "로컬 파일"])
video_file = None
youtube_url = None

if src_type == "유튜브 링크":
    youtube_url = st.text_input("유튜브 URL 입력")
else:
    video_file = st.file_uploader("영상 파일 업로드", type=["mp4", "mov", "mkv"])

if st.button("요약 시작"):
    if not api_key:
        st.error("API Key를 입력하세요 (또는 Streamlit Secrets 사용).")
        st.stop()

    client = get_client(api_key)

    with tempfile.TemporaryDirectory() as td:
        tdir = Path(td)

        if youtube_url:
            st.info("유튜브 오디오 다운로드 중...")
            audio_path = download_audio_from_youtube(youtube_url, tdir)
        elif video_file:
            st.info("영상에서 오디오 추출 중...")
            vpath = tdir / video_file.name
            with open(vpath, "wb") as f:
                f.write(video_file.read())
            audio_path = extract_audio(vpath, tdir / "audio.wav")
        else:
            st.error("영상 소스를 제공하세요.")
            st.stop()

        st.info("음성 → 텍스트 전사 중...")
        transcript = transcribe_audio(client, audio_path)

        st.info("부분 요약 생성 중...")
        chunks = chunk_text(transcript, CHUNK_CHAR_LEN)
        bullets = []
        progress = st.progress(0)
        for i, c in enumerate(chunks, 1):
            bullets.append(summarize_map(client, c, lang="한국어"))
            progress.progress(i / len(chunks))

        st.info("최종 요약 통합 중...")
        final_summary = summarize_reduce(client, bullets, lang="한국어")

        st.subheader("📌 최종 요약")
        st.markdown(final_summary)

        st.download_button(
            "📥 요약 다운로드 (txt)",
            data=final_summary,
            file_name="summary.txt",
            mime="text/plain",
        )
