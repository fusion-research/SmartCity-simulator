from .smart_city import SmartCity
from .engine import Engine
from .factory import build_all


def main():
    configs = {
        "energies": {
            "energies": [
                    {
                        "name": "Carbon",
                        "cost": 0.2,
                        "amount": 100,
                        "pollution_factor": 1,
                    },
                    {
                        "name": "Nuclear",
                        "cost": 0.5,
                        "amount": 40,
                        "pollution_factor": 0,
                    },
                    {
                        "name": "Renewable",
                        "cost": 1,
                        "amount": 10,
                        "pollution_factor": 0,
                    }
            ]
        },
        "people": {
            "nb_people": 500,
            "pollution_pref": {"distribution_name": "uniform", "low": 0., "high": 0.5},
            "nuclear_pref": {"distribution_name": "uniform", "low": 0.2, "high": 1.0},
            "lights_pref": "random",
            "heat_pref": "random"
        },
        "lights": 5_000,
        "heaters": 800
    }

    data = build_all(configs)
    local_vars = locals()
    local_vars = {**local_vars, **configs}
    smart_city = SmartCity(people=people, energies=energies,
                           lights=lights, heaters=heaters)
    engine = Engine(smart_city)


if __name__ == '__main__':
    main()
