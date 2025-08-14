import logging
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple, Union

from lhotse import fix_manifests, validate_recordings_and_supervisions
from lhotse.audio import Recording, RecordingSet
from lhotse.supervision import SupervisionSegment, SupervisionSet
from lhotse.recipes.utils import manifests_exist, read_manifests_if_cached
from lhotse.utils import Pathlike

from tqdm.auto import tqdm

def prepare_kaldi_style_dataset(
    corpus_dir: Pathlike,
    output_dir: Pathlike,
    dataset_parts: Union[str, Sequence[str]] = ("train", "dev", "test"),
    prefix: str = "tedlium",
    normalize_text: str = "none",
    num_jobs: int = 1,
) -> Dict[str, Dict[str, Union[RecordingSet, SupervisionSet]]]:
    """
    Prepare manifests from Kaldi-style dataset with wav.scp, text, utt2spk.

    :param corpus_dir: Path to data folder containing subfolders like train/, test/
    :param output_dir: Path to save manifests
    :param dataset_parts: Subfolders to process (e.g., 'train', 'test')
    :param prefix: prefix code, e.g., "as" for Assamese
    :param normalize_text: "none" or "lower"
    :param num_jobs: Not used here, but kept for API consistency
    :return: Dictionary of manifests keyed by dataset part
    """
    corpus_dir = Path(corpus_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if isinstance(dataset_parts, str):
        dataset_parts = [dataset_parts]

    manifests = {}

    for part in dataset_parts:
        part_dir = corpus_dir / part
        if not part_dir.is_dir():
            logging.warning(f"Dataset part dir not found: {part_dir}")
            continue

        # Read wav.scp: utt_id -> audio_path
        wav_scp_path = part_dir / "wav.scp"
        wav_dict = {}
        with open(wav_scp_path, "r", encoding="utf-8") as f:
            for line in f:
                utt_id, path = line.strip().split(None, 1)
                wav_dict[utt_id] = Path(path)

        # Read text: utt_id -> transcript
        text_path = part_dir / "text"
        text_dict = {}
        with open(text_path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(maxsplit=1)
                if len(parts) < 2:
                    continue
                utt_id, transcript = parts
                text_dict[utt_id] = transcript

        # Read utt2spk: utt_id -> speaker_id
        utt2spk_path = part_dir / "utt2spk"
        utt2spk_dict = {}
        with open(utt2spk_path, "r", encoding="utf-8") as f:
            for line in f:
                utt_id, spk_id = line.strip().split(None, 1)
                utt2spk_dict[utt_id] = spk_id

        recordings = []
        supervisions = []

        for utt_id in tqdm(wav_dict.keys(), desc=f"Processing {part} utterances"):
            if utt_id not in text_dict or utt_id not in utt2spk_dict:
                logging.warning(f"Missing text or utt2spk entry for {utt_id}, skipping.")
                continue

            audio_path = wav_dict[utt_id]
            if not audio_path.is_file():
                logging.warning(f"Audio file does not exist: {audio_path}, skipping.")
                continue

            recording = Recording.from_file(audio_path, recording_id=utt_id)
            transcript = text_dict[utt_id]
            if normalize_text == "lower":
                transcript = transcript.lower()

            supervision = SupervisionSegment(
                id=utt_id,
                recording_id=utt_id,
                start=0.0,
                duration=recording.duration,
                channel=0,
                language="en",
                speaker=utt2spk_dict[utt_id],
                text=transcript,
                alignment=None,
            )

            recordings.append(recording)
            supervisions.append(supervision)

        recording_set = RecordingSet.from_recordings(recordings)
        supervision_set = SupervisionSet.from_segments(supervisions)

        # Fix and validate
        recording_set, supervision_set = fix_manifests(recording_set, supervision_set)
        validate_recordings_and_supervisions(recording_set, supervision_set)

        # Save manifests
        recording_path = output_dir / f"{prefix}_recordings_{part}.jsonl.gz"
        supervision_path = output_dir / f"{prefix}_supervisions_{part}.jsonl.gz"

        recording_set.to_file(recording_path)
        supervision_set.to_file(supervision_path)

        manifests[part] = {
            "recordings": recording_set,
            "supervisions": supervision_set,
        }
        logging.info(f"Saved manifests for {part} to {output_dir}")

    return manifests


# Example usage:
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    corpus_dir = "data"
    output_dir = "data/manifests"
    prepare_kaldi_style_dataset(corpus_dir, output_dir, dataset_parts=["train", "dev", "test"], prefix="tedlium", normalize_text="lower")

