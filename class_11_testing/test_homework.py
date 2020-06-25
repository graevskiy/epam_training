import pytest

from homework import Dollar, Euro, Rubble

# explicitly set rates and acronyms for testing
CURRENCIES_RATES = list(zip([Dollar, Euro, Rubble], [2, 1, 100], ["USD", "EUR", "RUB"]))

# test by comparing with hardcoded values
def test_create_currency_correct():
    d = Dollar(100.0)
    assert d.__str__() == "100.0 USD"


def test_create_currency_correct_int():
    d = Dollar(100)
    assert d.__str__() == "100.0 USD"


def test_create_currency_incorrect_str():
    with pytest.raises(TypeError):
        Dollar("100")


def test_amount_property():
    r = Rubble(100)
    assert r.amount == 100.0


def test_to_correct():
    assert Rubble(100).to(Dollar) == Dollar(2)


def test_to_incorrect():
    with pytest.raises(AttributeError):
        Dollar(100).to("5")


# create a bit more automation with parametrization per function
@pytest.mark.parametrize(
    "test_currency,expected", zip([Dollar, Euro, Rubble], ["USD", "EUR", "RUB"])
)
def test_acr(test_currency, expected):
    assert test_currency.acr == expected


@pytest.mark.parametrize("currency,rate,acr", CURRENCIES_RATES)
def test_base_rate(currency, rate, acr):
    assert currency.base_rate == rate


@pytest.mark.parametrize("currency", [Dollar, Euro, Rubble])
def test_exchange_rate_incorrect_input(currency):
    with pytest.raises(AttributeError):
        currency.exchange_rate(5)


@pytest.mark.parametrize("currency", [Dollar, Euro, Rubble])
def test_course_incorrect_input(currency):
    with pytest.raises(AttributeError):
        currency.course("5")


def test_equal_correct():
    assert Dollar(100) == Euro(50)


def test_equal_incorrect():
    with pytest.raises(AttributeError):
        Dollar(100) == 100


def test_lt_correct():
    assert Dollar(10) < Dollar(11)


def test_lt_corect_neg():
    assert Dollar(-10) < Dollar(-9)


def test_lt_incorrect():
    with pytest.raises(AttributeError):
        Dollar(10) < 20


@pytest.mark.parametrize("right_part", [50, Dollar(50), Euro(25)])
def test_add_correct(right_part):
    assert Dollar(50) + right_part == Dollar(100)


def test_add_incorrect():
    with pytest.raises(TypeError):
        Dollar(50) + "50"


@pytest.mark.parametrize("left_part", [50, Dollar(50), Euro(25)])
def test_radd_correct(left_part):
    assert left_part + Dollar(50) == Dollar(100)


def test_radd_incorrect():
    with pytest.raises(TypeError):
        "20" + Dollar(50)


# group functions which use permutations of all currencies and their attrs
@pytest.mark.parametrize("from_", CURRENCIES_RATES)
@pytest.mark.parametrize("to", CURRENCIES_RATES)
class TestWithPerms:
    def test_exchange_rate_correct(self, from_, to):
        from_, from_rate, _ = from_
        to, to_rate, _ = to
        assert from_.exchange_rate(to) == to_rate / from_rate

    def test_course_correct(self, from_, to):
        from_, from_rate, from_acr = from_
        to, to_rate, to_acr = to
        rate = to_rate / from_rate
        assert from_.course(to) == f"{rate} {to_acr} for 1 {from_acr}"

    def test_to_correct(self, from_, to):
        from_, from_rate, _ = from_
        to, to_rate, to_acr = to
        n = 127
        res = n * to_rate / from_rate
        assert from_(n).to(to).__str__() == f"{res} {to_acr}"
