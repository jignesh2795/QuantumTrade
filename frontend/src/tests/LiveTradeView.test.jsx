import { render, screen } from "@testing-library/react";
import LiveTradeView from "../components/LiveTradeView";

test("renders live trade view component", () => {
  render(<LiveTradeView />);
  const tradeViewElement = screen.getByText(/Live Trading/i);
  expect(tradeViewElement).toBeInTheDocument();
});
