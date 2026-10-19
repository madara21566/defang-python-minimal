import asyncio
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

log = logging.getLogger("skill-monitor")


class SkillMonitorDemo:
    def __init__(self, cooldown_seconds=5.0, poll_interval=0.5):
        self.cooldown_seconds = float(cooldown_seconds)
        self.poll_interval = float(poll_interval)
        self.skill_available = True
        self.cooldown_ends_at = 0.0
        self.running = False

    async def read_skill_state(self):
        """Simulated skill availability check."""
        now = time.monotonic()

        if (
            not self.skill_available
            and now >= self.cooldown_ends_at
        ):
            self.skill_available = True
            log.info("DEMO: Cooldown complete; skill available")

        return self.skill_available

    async def activation_event(self):
        """Simulates an activation event; does not activate the game skill."""
        if not self.skill_available:
            return False

        log.info("DEMO: Skill activation event")

        self.skill_available = False
        self.cooldown_ends_at = (
            time.monotonic() + self.cooldown_seconds
        )

        log.info(
            "DEMO: Cooldown started for %.1f seconds",
            self.cooldown_seconds
        )

        return True

    async def run(self):
        self.running = True

        log.info("Skill monitor demo started")

        try:
            while self.running:
                available = await self.read_skill_state()

                if available:
                    await self.activation_event()

                await asyncio.sleep(self.poll_interval)

        except asyncio.CancelledError:
            raise

        finally:
            self.running = False
            log.info("Skill monitor demo stopped")

    def stop(self):
        self.running = False


async def main():
    demo = SkillMonitorDemo(
        cooldown_seconds=5,
        poll_interval=0.5
    )

    await demo.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSkill monitor stopped.")
