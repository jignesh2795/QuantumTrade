import { render, screen } from "@testing-library/react";
import App from "../App";

test("renders QuantumTrade app", () => {
  render(<App />);
  const linkElement = screen.getByText(/QuantumTrade/i);
  expect(linkElement).toBeInTheDocument();
});
