import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1

    # Test all combinations of a, b, c
    for i in range(8):  # 3-bit inputs
        dut.ui_in.value = i

        await ClockCycles(dut.clk, 1)

        a = (i >> 0) & 1
        b = (i >> 1) & 1
        c = (i >> 2) & 1

        expected_sum = a ^ b ^ c
        expected_carry = (a & b) | (b & c) | (a & c)

        val = dut.uo_out.value.integer

        actual_sum = (val >> 1) & 1
        actual_carry = (val >> 0) & 1

        assert actual_sum == expected_sum, f"SUM mismatch for input {i}"
        assert actual_carry == expected_carry, f"CARRY mismatch for input {i}"
