from app import app
import os
import settings
from dotenv import load_dotenv
# from dapr.actor import ActorInterface, actormethod
from dapr.actor.runtime.config import (
    ActorRuntimeConfig,
    ActorReentrancyConfig,
)  # , ActorTypeConfig
from flask_dapr.actor import DaprActor

# from dapr.conf import settings
from dapr_config.demo_actor import DemoActor


# Enable DaprActor Extension
actor = DaprActor(app)
app.config.from_object(settings)

# Register DemoActor
actor.register_actor(DemoActor)

# Create ActorRuntime configuration
# actor_runtime_config = ActorRuntimeConfig(
#    actor_idle_timeout=timedelta(hours=1),
#    actor_scan_interval=timedelta(seconds=30),
#    drain_ongoing_call_timeout=timedelta(minutes=1),
#    drain_rebalanced_actors=True,
#    reentrancy=ActorReentrancyConfig(enabled=False),
#    reminders_storage_partitions=7
# )


load_dotenv()

if __name__ == "__main__":
    app.run(
        host=app.config["APPLICATION_HOST"],
        debug=True,
        port=app.config["APPLICATION_PORT"],
    )
