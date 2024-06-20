#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>
#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/udp.h>

#define QUIC_PORT 443

// New destination IP address in hexadecimal (3.142.37.65)
#define DEST_IP 0x038E2541

'''
Check count of recieved packets using:

sudo bpftool map show
sudo bpftool map dump id [map_id]
'''

// Define a map to hold packet counts
struct {
    __uint(type, BPF_MAP_TYPE_ARRAY);
    __type(key, u32);
    __type(value, u64);
    __uint(max_entries, 2);
} packet_count SEC(".maps");

enum stats {
    RECEIVED,
    FORWARDED,
};

SEC("xdp_quic_forwarder")
int xdp_prog_simple(struct xdp_md *ctx) {
    void *data_end = (void *)(long)ctx->data_end;
    void *data = (void *)(long)ctx->data;

    struct ethhdr *eth = data;
    if ((void *)eth + sizeof(*eth) > data_end)
        return XDP_DROP; // Drop packet if it does not contain a full Ethernet header

    struct iphdr *ip = data + sizeof(*eth);
    if ((void *)ip + sizeof(*ip) > data_end)
        return XDP_DROP; // Drop packet if it does not contain a full IP header

    if (ip->protocol != IPPROTO_UDP)
        return XDP_PASS; // Ignore non-UDP packets

    struct udphdr *udp = (void *)ip + sizeof(*ip);
    if ((void *)udp + sizeof(*udp) > data_end)
        return XDP_DROP; // Drop packet if it does not contain a full UDP header

    // Increase the packet received counter
    u32 key = RECEIVED;
    u64 *value = bpf_map_lookup_elem(&packet_count, &key);
    if (value) {
        (*value)++;
    }

    if (udp->dest != bpf_htons(QUIC_PORT))
        return XDP_PASS; // Ignore UDP packets that are non-QUIC

    // Change the IP destination address
    ip->daddr = bpf_htonl(DEST_IP);

    // Recalculate the IP checksum
    bpf_l3_csum_replace(ctx, offsetof(struct iphdr, check), 0, ip->daddr, sizeof(ip->daddr));

    // Increase packet counter
    key = FORWARDED;
    value = bpf_map_lookup_elem(&packet_count, &key);
    if (value) {
        (*value)++;
    }

    return XDP_TX; // Forward the packet out through same interface
}

char _license[] SEC("license") = "GPL";
