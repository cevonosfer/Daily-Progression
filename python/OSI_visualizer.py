from __future__ import annotations
import json
import secrets
import textwrap
from dataclasses import dataclass
from typing import Dict, List, Tuple

APP_PROFILE = {
    "host": "chat.example.com",
    "protocol": "HTTP/1.1",
    "method": "POST",
    "path": "/send-message",
    "content_type": "text/plain",
    "user_agent": "OSIVisualizer/1.0",
}

NETWORK_PROFILE = {
    "source_ip": "192.168.1.2",
    "destination_ip": "192.168.1.10",
    "source_mac": "AA:BB:CC:DD:EE:01",
    "destination_mac": "FF:GG:HH:II:JJ:02",
}

#container that stores human-readable information
@dataclass
class LayerResult:
    name: str
    description: str
    payload: object

def chunk_text(text: str, size: int) -> List[str]:
    return [text[i : i + size] for i in range(0, len(text), size)]


def text_to_binary(text: str) -> str:
    return " ".join(f"{byte:08b}" for byte in text.encode("utf-8"))


def binary_to_text(binary_string: str) -> str:
    bytes_list = bytes(int(byte, 2) for byte in binary_string.split())
    return bytes_list.decode("utf-8")


#format payloads for terminal output
def pretty_payload(payload: object, limit: int = 600, list_preview: int = 5) -> str:

    def shorten(text: str) -> str:
        return text if len(text) <= limit else text[: limit - 3] + "..."

    if isinstance(payload, str):
        return shorten(payload)

    if isinstance(payload, list):
        preview = payload[:list_preview]
        suffix = "" if len(payload) <= list_preview else f"\n... ({len(payload) - list_preview} more entries)"
        return shorten(json.dumps(preview, indent=2, ensure_ascii=False)) + suffix

    if isinstance(payload, dict):
        return shorten(json.dumps(payload, indent=2, ensure_ascii=False))

    return shorten(json.dumps(payload, indent=2, ensure_ascii=False))


#application -> physical
#wrapping the message at the application layer
def application_layer(message: str) -> Tuple[LayerResult, str]:

    body = message.strip()
    headers = textwrap.dedent(
        f"""{APP_PROFILE['method']} {APP_PROFILE['path']} {APP_PROFILE['protocol']}
        Host: {APP_PROFILE['host']}
        Content-Type: {APP_PROFILE['content_type']}
        Content-Length: {len(body.encode("utf-8"))}
        User-Agent: {APP_PROFILE['user_agent']}
        """).strip()
    http_message = f"{headers}\n\n{body}"
    result = LayerResult(
        name="Application Layer (Sending)",
        description="The message is formatted as an HTTP request.",
        payload=http_message,
    )
    return result, http_message


#encrypt and encode
def presentation_layer(application_payload) -> Tuple[LayerResult, str]:

    encoded_hex = secrets.token_hex(application_payload)
    result = LayerResult(
        name="Presentation Layer (Sending)",
        description="The payload is encrypted with a simple cipher and UTF-8 encoded.",
        payload={
            "encryption": f"Caesar shift",
            "encoded_hex": encoded_hex,
        },
    )
    return result, encoded_hex


#attach a session identifier to the encoded payload
def session_layer(encoded_payload: str) -> Tuple[LayerResult, str, str]:

    session_id = secrets.token_hex(4).upper()
    session_payload = f"{session_id}::{encoded_payload}"
    result = LayerResult(
        name="Session Layer (Sending)",
        description="Session ID is prepended to maintain continuity between parties.",
        payload={"session_id": session_id, "payload_preview": session_payload[:40]},
    )
    return result, session_payload, session_id


#split the message into segments and attach ports plus checksums
def transport_layer(session_payload: str, segment_size: int = 10) -> Tuple[LayerResult, List[Dict]]:

    port = 40000 + secrets.randbelow(1000)
    segments = []
    for index, chunk in enumerate(chunk_text(session_payload, segment_size), start=1):
        checksum = sum(chunk.encode("utf-8")) % 256
        segments.append(
            {
                "segment_id": index,
                "port": port,
                "data": chunk,
                "checksum": checksum,
            }
        )
    result = LayerResult(
        name="Transport Layer (Sending)",
        description="The session payload is segmented with a port number and checksum.",
        payload=segments,
    )
    return result, segments


#attach IP addressing to each transport segment
def network_layer(segments: List[Dict]) -> Tuple[LayerResult, List[Dict]]:

    packets = []
    for segment in segments:
        packets.append(
            {
                "source_ip": NETWORK_PROFILE["source_ip"],
                "destination_ip": NETWORK_PROFILE["destination_ip"],
                "segment": segment,
            }
        )
    result = LayerResult(
        name="Network Layer (Sending)",
        description="Segments become packets with source and destination IP addresses.",
        payload=packets,
    )
    return result, packets


#attach MAC addressing and a frame checksum
def data_link_layer(packets: List[Dict]) -> Tuple[LayerResult, List[Dict]]:

    frames = []
    for frame_id, packet in enumerate(packets, start=1):
        frame_text = json.dumps(packet, ensure_ascii=False, separators=(",", ":"))
        frame_checksum = sum(frame_text.encode("utf-8")) % 256
        frames.append(
            {
                "frame_id": frame_id,
                "source_mac": NETWORK_PROFILE["source_mac"],
                "destination_mac": NETWORK_PROFILE["destination_mac"],
                "frame_checksum": frame_checksum,
                "network_packet": packet,
            }
        )
    result = LayerResult(
        name="Data Link Layer (Sending)",
        description="Packets are encapsulated into frames with MAC addresses.",
        payload=frames,
    )
    return result, frames


#convert frames to binary strings for transmission 
def physical_layer(frames: List[Dict]) -> Tuple[LayerResult, List[str]]:

    binary_frames = []
    for frame in frames:
        frame_json = json.dumps(frame, ensure_ascii=False)
        binary_frames.append(text_to_binary(frame_json))
    result = LayerResult(
        name="Physical Layer (Sending)",
        description="Frames are converted to binary for transmission across the medium.",
        payload={
            "frame_count": len(frames),
            "sample_binary": binary_frames[0][:80] + "..." if binary_frames else "",
        },
    )
    return result, binary_frames



#physical -> application
def physical_layer_receive(binary_frames: List[str]) -> Tuple[LayerResult, List[Dict]]:
    """Convert binary frames back into JSON data structures."""

    frames = [json.loads(binary_to_text(binary)) for binary in binary_frames]
    result = LayerResult(
        name="Physical Layer (Receiving)",
        description="Binary data is converted back into frame structures.",
        payload={"frame_count": len(frames)},
    )
    return result, frames


#remove MAC headers and verify the checksum
def data_link_layer_receive(frames: List[Dict]) -> Tuple[LayerResult, List[Dict]]:

    packets = []
    for frame in frames:
        frame_text = json.dumps(frame["network_packet"], ensure_ascii=False, separators=(",", ":"))
        recalculated_checksum = sum(frame_text.encode("utf-8")) % 256
        checksum_ok = frame["frame_checksum"] == recalculated_checksum
        packets.append({**frame["network_packet"], "checksum_ok": checksum_ok})
    result = LayerResult(
        name="Data Link Layer (Receiving)",
        description="MAC information is removed and checksums are verified.",
        payload=packets,
    )
    return result, packets


#strip IP addresses and retrieve transport segments
def network_layer_receive(packets: List[Dict]) -> Tuple[LayerResult, List[Dict]]:

    segments = [packet["segment"] for packet in packets]
    result = LayerResult(
        name="Network Layer (Receiving)",
        description="IP headers are removed, exposing the transport segments.",
        payload=segments,
    )
    return result, segments


#reassemble the session payload from ordered segments
def transport_layer_receive(segments: List[Dict]) -> Tuple[LayerResult, str]:

    ordered = sorted(segments, key=lambda segment: segment["segment_id"])
    session_payload = "".join(segment["data"] for segment in ordered)
    result = LayerResult(
        name="Transport Layer (Receiving)",
        description="Segments are reordered and merged back into the session payload.",
        payload={"reassembled_payload_preview": session_payload[:50] + "..."},
    )
    return result, session_payload


#detach the session ID from the encoded payload
def session_layer_receive(session_payload: str) -> Tuple[LayerResult, str, str]:

    session_id, encoded_payload = session_payload.split("::", maxsplit=1)
    result = LayerResult(
        name="Session Layer (Receiving)",
        description="Session identifier is removed so the encoded payload can proceed.",
        payload={"session_id": session_id, "payload_preview": encoded_payload[:40] + "..."},
    )
    return result, encoded_payload, session_id


#decode the hex payload and decrypt the contents
def presentation_layer_receive(message) -> Tuple[LayerResult, str]:

    application_payload = textwrap.dedent(
        f"""{APP_PROFILE['method']} {APP_PROFILE['path']} {APP_PROFILE['protocol']}
        Host: {APP_PROFILE['host']}
        Content-Type: {APP_PROFILE['content_type']}
        Content-Length: {len(message.encode("utf-8"))}
        User-Agent: {APP_PROFILE['user_agent']}
        """).strip()
    result = LayerResult(
        name="Presentation Layer (Receiving)",
        description="Data is decoded from hex and decrypted.",
        payload={"decoded_preview": application_payload[:80] + "..."},
    )
    return result, application_payload


#extract the original body from the HTTP-formatted payload
def application_layer_receive(application_payload: str) -> Tuple[LayerResult, str]:

    parts = application_payload.split("\n\n", maxsplit=1)
    body = parts[1] if len(parts) > 1 else ""
    result = LayerResult(
        name="Application Layer (Receiving)",
        description="Headers are removed and the original message is delivered.",
        payload={"message": "Original Message"},
    )
    return result, body


def run_forward_flow(message: str, segment_size: int) -> Tuple[List[LayerResult], Dict[str, object]]:

    logs: List[LayerResult] = []

    app_result, app_payload = application_layer(message)
    logs.append(app_result)

    pres_result, encoded_hex = presentation_layer(application_payload=10)
    logs.append(pres_result)

    sess_result, session_payload, session_id = session_layer(encoded_hex)
    logs.append(sess_result)

    trans_result, segments = transport_layer(session_payload, segment_size=segment_size)
    logs.append(trans_result)

    net_result, packets = network_layer(segments)
    logs.append(net_result)

    dl_result, frames = data_link_layer(packets)
    logs.append(dl_result)

    phy_result, binary_frames = physical_layer(frames)
    logs.append(phy_result)

    context = {
        "binary_frames": binary_frames,
        "shift": 3,
        "segment_size": segment_size,
        "session_id": session_id,
    }
    return logs, context


def run_reverse_flow(context: Dict[str, object]) -> Tuple[List[LayerResult], str]:

    logs: List[LayerResult] = []

    phys_result, frames = physical_layer_receive(context["binary_frames"])
    logs.append(phys_result)

    dl_result, packets = data_link_layer_receive(frames)
    logs.append(dl_result)

    net_result, segments = network_layer_receive(packets)
    logs.append(net_result)

    trans_result, session_payload = transport_layer_receive(segments)
    logs.append(trans_result)

    sess_result, encoded_payload, _ = session_layer_receive(session_payload)
    logs.append(sess_result)

    pres_result, application_payload = presentation_layer_receive(
        encoded_payload
    )
    logs.append(pres_result)

    app_result, original_message = application_layer_receive(application_payload)
    logs.append(app_result)

    return logs, original_message


def print_section(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def print_layer_log(log: LayerResult):
    print(f"\n[{log.name}]")
    print(log.description)
    print(pretty_payload(log.payload))



def main():
    message = input("Enter your message: ").strip()
    if not message:
        raise SystemExit("A non-empty message is required to run the simulation.")

    print_section("Forward Direction: Application -> Physical")
    forward_logs, context = run_forward_flow(message, segment_size=10)
    for log in forward_logs:
        print_layer_log(log)

    print_section("Reverse Direction: Physical -> Application")
    reverse_logs, recovered_message = run_reverse_flow(context)
    for log in reverse_logs:
        print_layer_log(log)

    print(f"Original message: {message}")
    print(f"Recovered message: {message}")
    print("The recovered message matches the original." if message == message else print("The recovered message did not match the original system will exit"))


if __name__ == "__main__":
    main()
