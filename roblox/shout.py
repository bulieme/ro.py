from datetime import datetime

import iso8601

from .bases.basegroup import BaseGroup
from .partials.partialuser import PartialUser
from .utilities.shared import ClientSharedObject


class Shout:
    def __init__(self, shared: ClientSharedObject,
                 group: BaseGroup, raw_data: dict = None):
        self._shared = shared

        self._requests = shared.requests
        """A client shared object."""
        self.group: BaseGroup = group
        """The group the shout belongs to."""
        if raw_data is not None:
            self.body: str = raw_data['body']
            """What the shout contains."""
            self.created: datetime = iso8601.parse_date(raw_data['created'])
            """When the first shout was created."""
            self.updated: datetime = iso8601.parse_date(raw_data['updated'])
            """When the latest shout was created."""
            self.poster: PartialUser = PartialUser(cso, raw_data['poster'])
            """The user who posted the shout."""

    async def set(self, new_body: str) -> int:
        """
        Updates the shout
        Parameters
        ----------
        new_body : str
            What the shout will be updated to.
        Returns
        -------
        int
        """
        response = await self._requests.post(
            url=self._shared.url_generator.get_url("groups", f"v1/groups/{self.group.id}/status"),
            json={
                "message": new_body
            }
        )
        return response.status_code

    async def delete(self) -> int:
        """
        Deletes the shout.
        Returns
        -------
        str
        """
        return await self.set("")