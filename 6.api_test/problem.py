import pandas as pd
import pulp


class CarGroupProblem:
    def __init__(self, student_df, car_df, name="ClubCarProblem"):
        self.student_df = student_df
        self.car_df = car_df
        self.name = name
        self.prob = self._formulate()

    def _formulate(self):
        prob = pulp.LpProblem(self.name, pulp.LpMinimize)
        S = self.student_df["student_id"].tolist()
        C = self.car_df["car_id"].tolist()
        G = [1, 2, 3, 4]
        SC = [(s, c) for s in S for c in C]
        S_license = self.student_df[self.student_df.license == 1]["student_id"]
        S_g = {g: self.student_df[self.student_df.grade == g]["student_id"] for g in G}
        S_male = self.student_df[self.student_df.gender == 0]["student_id"]
        S_female = self.student_df[self.student_df.gender == 1]["student_id"]
        U = self.car_df["capacity"].tolist()
        X = pulp.LpVariable.dicts("x", SC, cat="Binary")

        for s in S:
            prob += pulp.lpSum([X[s, c] for c in C]) == 1

        for c in C:
            prob += pulp.lpSum([X[s, c] for s in S]) <= U[c]
            prob += pulp.lpSum(X[s, c] for s in S_license) >= 1
            prob += pulp.lpSum(X[s, c] for s in S_male) >= 1
            prob += pulp.lpSum(X[s, c] for s in S_female) >= 1

            for g in G:
                prob += pulp.lpSum(X[s, c] for s in S_g[g]) >= 1

        return {"prob": prob, "variable": {"X": X}, "list": {"S": S, "C": C}}

    def solve(self):
        status = self.prob['prob'].solve()
        X = self.prob['variable']["X"]
        S = self.prob["list"]["S"]
        C = self.prob["list"]["C"]
        car2studnets = {c: [s for s in S if X[s, c].value() == 1] for c in C}
        student2car = {s: c for c, ss in car2studnets.items() for s in ss}
        solution_df = pd.DataFrame(list(student2car.items()), columns=["student_id", "car_id"])
        return solution_df

if __name__ == '__main__':
    student_df = pd.read_csv("./resource/students.csv")
    car_df = pd.read_csv("./resource/cars.csv")
    prob = CarGroupProblem(student_df, car_df)
    solution_df = prob.solve()
    print(f"Solution:\n {solution_df}")