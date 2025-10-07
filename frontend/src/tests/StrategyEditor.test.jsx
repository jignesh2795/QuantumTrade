import { render, screen } from "@testing-library/react";
import StrategyEditor from "../components/StrategyEditor";

test("renders strategy editor component", () => {
  render(<StrategyEditor />);
  const editorElement = screen.getByText(/Strategy Editor/i);
  expect(editorElement).toBeInTheDocument();
});
