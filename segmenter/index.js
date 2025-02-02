function segmentTranscription(transcription, segmentDuration = 30) {
    const utterances = transcription.transcription.utterances;
    const segments = [];
    let currentSegment = "";
    let segmentStart = utterances.length > 0 ? utterances[0].start : 0;
    let segmentEnd = 0;

    for (const utterance of utterances) {
        const start = utterance.start;
        const end = utterance.end;
        const text = utterance.text;

        if (end - segmentStart <= segmentDuration) {
            currentSegment += text + " ";
            segmentEnd = end;
        } else {
            segments.push({
                start: segmentStart,
                end: segmentEnd,
                text: currentSegment.trim()
            });
            currentSegment = text + " ";
            segmentStart = start;
            segmentEnd = end;
        }
    }

    if (currentSegment) {
        segments.push({
            start: segmentStart,
            end: segmentEnd,
            text: currentSegment.trim()
        });
    }

    return segments;
}

document.getElementById('segmentButton').addEventListener('click', () => {
    const inputText = document.getElementById('inputText').value;
    const segmentDuration = parseInt(document.getElementById('segmentDuration').value, 10);
    const json = JSON.parse(inputText);
    const segments = segmentTranscription(json, segmentDuration);
    const outputDiv = document.getElementById('outputSegments');
    outputDiv.innerHTML = segments.map(segment => `<pre>${JSON.stringify(segment, null, 2)}</pre>`).join('');
});

document.getElementById('copyButton').addEventListener('click', () => {
    const outputDiv = document.getElementById('outputSegments');
    const range = document.createRange();
    range.selectNode(outputDiv);
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(range);
    document.execCommand('copy');
    window.getSelection().removeAllRanges();
});
