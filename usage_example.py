from compact_frame_format import Cff

# Create and send frames
messages = ["Hello", "World", "CFF"]
buffer = bytearray()

cff = Cff()

print("Creating frames:")
for i, message in enumerate(messages):
    payload = message.encode("utf-8")
    frame = cff.create(payload)

    print(f"  Frame {i}: {message} -> {len(frame)} bytes")

    # Simulate adding to receive buffer
    buffer.extend(frame)

print(f"\nBuffer contains {len(buffer)} bytes total")

# Parse all frames from buffer
received_frames, consumed_bytes = cff.parse_frames(bytes(buffer))

print(f"\nProcessed {consumed_bytes} bytes from buffer")
print("Received frames:")
for frame in received_frames:
    message = frame.payload.decode("utf-8")
    print(f"  Frame {frame.frame_counter}: {message}")
