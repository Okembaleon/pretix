#
# This file is part of pretix (Community Edition).
#
# Copyright (C) 2014-2020 Raphael Michel and contributors
# Copyright (C) 2020-2021 rami.io GmbH and contributors
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General
# Public License as published by the Free Software Foundation in version 3 of the License.
#
# ADDITIONAL TERMS APPLY: Pursuant to Section 7 of the GNU Affero General Public License, additional terms are
# applicable granting you additional permissions and placing additional restrictions on your usage of this software.
# Please refer to the pretix LICENSE file to obtain the full terms applicable to this work. If you did not receive
# this file, see <https://pretix.eu/about/en/license>.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License along with this program.  If not, see
# <https://www.gnu.org/licenses/>.
#
from dateutil.rrule import rrulestr
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

# This file is based on an earlier version of pretix which was released under the Apache License 2.0. The full text of
# the Apache License 2.0 can be obtained at <http://www.apache.org/licenses/LICENSE-2.0>.
#
# This file may have since been changed and any changes are released under the terms of AGPLv3 as described above. A
# full history of changes and contributors is available at <https://github.com/pretix/pretix>.
#
# This file contains Apache-licensed contributions copyrighted by: Christopher Dambamuromo, Sohalt
#
# Unless required by applicable law or agreed to in writing, software distributed under the Apache License 2.0 is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under the License.


class BanlistValidator:

    banlist = []

    def __call__(self, value):
        # Validation logic
        if value in self.banlist:
            raise ValidationError(
                _('This field has an invalid value: %(value)s.'),
                code='invalid',
                params={'value': value},
            )


@deconstructible
class EventSlugBanlistValidator(BanlistValidator):

    banlist = [
        'download',
        'healthcheck',
        'locale',
        'control',
        'redirect',
        'jsi18n',
        'metrics',
        '_global',
        '__debug__',
        'api',
        'events',
        'csp_report',
        'widget',
        'customer',
        'account',
    ]


@deconstructible
class OrganizerSlugBanlistValidator(BanlistValidator):

    banlist = [
        'download',
        'healthcheck',
        'locale',
        'control',
        'pretixdroid',
        'redirect',
        'jsi18n',
        'metrics',
        '_global',
        '__debug__',
        'about',
        'api',
        'csp_report',
        'widget',
    ]


@deconstructible
class EmailBanlistValidator(BanlistValidator):

    banlist = [
        settings.PRETIX_EMAIL_NONE_VALUE,
    ]


def multimail_validate(val):
    s = val.split(',')
    for part in s:
        validate_email(part.strip())
    return s


class RRuleValidator:
    def __call__(self, value):
        try:
            rrulestr(value)
        except Exception:
            raise ValidationError("Not a valid rrule.")
