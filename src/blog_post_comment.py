# N8, An amalgamation of personal code
# Copyright (C) 2024 Nathaniel Wright
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from datetime import datetime
from uuid import UUID
class BlogPostComment:
    created_date: datetime
    comment: str
    commenter: str
    id: UUID
    post_id: UUID

    def __init__(self, id: UUID, post_id: UUID, created_date: datetime, comment: str, commenter: str):
        self.id = id
        self.post_id = post_id
        self.created_date = created_date
        self.comment = comment
        self.commenter = commenter
