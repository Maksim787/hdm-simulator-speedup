from pathlib import Path
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset

from trainer.utils import seed_everything


DATA_PATH = Path("data_prepared/")


def get_parameters(df: pd.DataFrame) -> pd.DataFrame:
    # TODO: apply log-scale
    return df[[col for col in df.columns if col.isupper()]]


def get_results(df: pd.DataFrame) -> pd.DataFrame:
    df = df[[col for col in df.columns if not col.isupper() and col != "no."]]
    # assert df.isna().sum().sum() == 0, df.isna().sum(
    for col in df:
        if df[col].dtype == object:
            assert len(df[col].unique()) == 1, f"{df[col].unique()}"
            df = df.drop(columns=[col])
    return df


def split_main_other_simulations(df: pd.DataFrame) -> tuple[pd.Series, pd.DataFrame]:
    return df.iloc[0:1], df.iloc[1:]


def calculate_errors(main_results, other_results) -> float:
    # assert ((main_results >= 0).all(axis=0) | (main_results <= 0).all(axis=0)).all()
    # assert ((other_results >= 0).all(axis=0) | (other_results <= 0).all(axis=0)).all()
    assert (main_results.columns == other_results.columns).all()
    assert len(main_results) == 1
    # Calculate absolute errors
    abs_errors = other_results.sub(main_results.iloc[0], axis=1).abs()

    # Calculate relative errors, handling division by zero
    rel_errors = abs_errors.div(main_results.iloc[0].abs(), axis=1)
    rel_errors = rel_errors.map(lambda x: 0 if not np.isfinite(x) else x)
    return rel_errors


def get_parameters_with_errors(df, verbose: bool):
    # Split into main and other simulations
    main_df, other_df = split_main_other_simulations(df.fillna(0))
    prev_len = len(other_df)
    assert other_df.notna().all().all()
    # Check that main simulation has default parameters
    # assert get_parameters(main_df).isna().all().all()
    # Get results from simulations
    main_results = get_results(main_df)
    other_results = get_results(other_df)
    # Calculate errors
    errors = calculate_errors(main_results, other_results)
    # Sum errors across different fields
    errors = errors.sum(axis=1).rename("Error")
    assert errors.notna().all().all()
    # Construct final dataframe
    parameters_with_errors = pd.concat((get_parameters(other_df), errors), axis=1)
    # Drop NaNs
    prev_len = len(parameters_with_errors)
    assert parameters_with_errors.notna().all().all()
    assert len(parameters_with_errors) > 0
    return parameters_with_errors


def load_data(table_path: Path, verbose: bool):
    # Load the data from a CSV file
    df = pd.read_csv(table_path)

    # Calculate Errors for each parameter set
    try:
        df = get_parameters_with_errors(df, verbose=verbose)
    except:
        display(df)
        raise
    X = df.drop(columns=["Error"])
    y = df["Error"]

    # Convert to tensors
    X = torch.tensor(X.values, dtype=torch.float32)
    y = torch.tensor(y.values, dtype=torch.float32)

    return X, y


def get_dataloaders(data_path: Path = DATA_PATH, table: int = 0, test_size: float = 0.2, seed: int = 1, batch_size: int = 256, verbose: bool = False) -> tuple[DataLoader, DataLoader]:
    assert data_path.exists()
    table_path = data_path / f"table_{table}.csv"
    assert table_path.exists()

    X, y = load_data(table_path, verbose=verbose)

    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, shuffle=True, random_state=seed)
    assert y_train.ndim == 1 and y_test.ndim == 1
    in_features, out_features = X_train.shape[1], 1

    # Create TensorDataset
    train_dataset = TensorDataset(X_train, y_train)
    test_dataset = TensorDataset(X_test, y_test)

    # Create DataLoader
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, test_loader, in_features, out_features


def test(print_full_tensors: bool = True):
    train_loader, test_loader, in_features, out_features = get_dataloaders(verbose=True)
    print(f"{in_features = }; {out_features = }")
    print([a.size() for a in next(iter(train_loader))])
    if print_full_tensors:
        print([a for a in next(iter(train_loader))])
